from jobs.models import Job, Current_Worker, House, Request_Payment
from django.contrib.auth.models import User
import datetime
import pytz

class Customer:
    """
    Creates an object for customers to view jobs and houses of different status
    customer: a User object representing the customer
    houses: a queryset of all houses that belong to the customer
    """
    #filter results by the last week
    #note: add 1 day to 'today' because time seems to lag in the server
    today = datetime.datetime.now() + datetime.timedelta(days=2)
    start_delta = datetime.timedelta(days=today.weekday()+4)
    start_week = today.replace(hour=17, minute=0, second=0) - start_delta #start week is at 5:00PM one week back

    #allow datetime to be aware
    utc = pytz.UTC
    start_week = start_week.replace(tzinfo=utc)
    today = today.replace(tzinfo=utc)

    def __init__(self, customer):
        #get customer user object if current user is a worker or staff
        if customer.groups.filter(name__in=['Customers Staff', 'Workers']).exists():
            customer_id = customer.groups.values_list('name', flat=True)[1]
            if customer_id == 'Customers Staff' or customer_id == 'Workers':
                customer_id = customer.groups.values_list('name', flat=True)[0]
            customer_id = int(customer_id)
            self.customer = User.objects.get(pk=customer_id)
        else:
            self.customer = customer
        self.houses = self.houses()

    #gets attributes of objects up to two levels down
    def attribute_level(self, obj, compare={}):
        level = list(compare.keys())
        attribute = list(compare.values())

        if level[0] is not 0:
            if level[0] is 1:
                return getattr(obj, attribute[0])
            elif level[0] is 2:
                return getattr(getattr(obj, attribute[0][0]), attribute[0][1])
        else:
            return obj

    #reduces repetition of looping code to get a query set
    def get_queryset(self, append_outer=False, houses=[], queryset=[], compare=[]):
        for h in houses:
            for q in queryset.iterator():
                #get attributes to compare
                a = self.attribute_level(obj=h, compare=compare[0])
                b = self.attribute_level(obj=q, compare=compare[1])
                if a == b:
                    if append_outer == True:
                        yield h
                    else:
                        yield q

    def current_week_results(self, houses, queryset, model, update_field={}, **kwargs):
        """fetch current 2 week results, if there are none
        then set the appropriate house attributes to false"""
        for h in houses.iterator():
            for q in queryset.iterator():
                if q.house == h:
                    query_set_check = model.objects.filter(house=h, **kwargs)
                    if query_set_check:
                        setattr(h, list(update_field.keys())[0], list(update_field.values())[0][0])
                        h.save(update_fields=[list(update_field.keys())[0]])
                        yield h
                        break
                    else:
                        setattr(h, list(update_field.keys())[0], list(update_field.values())[0][1])
                        h.save(update_fields=[list(update_field.keys())[0]])

    #returns all houses that belong to the customer
    def houses(self):
        return House.objects.filter(customer=self.customer)

    """Current(Active) Houses"""
    #returns houses that are activley being worked on by workers
    def current_houses(self):
        """compare house with active jobs to customer house
        if the houses are the same, then it is a current customer house"""
        sql = 'SELECT * FROM jobs_current_worker WHERE current=1 GROUP BY house_id'
        current_houses = Current_Worker.objects.raw(sql)

        return self.get_queryset(append_outer=True, houses=current_houses, queryset=self.houses, compare=[{1: 'house'}, {0: 0}])

    #returns all approved jobs for houses for each customer
    def approved_jobs(self):
        return Job.objects.filter(house__customer=self.customer, approved=True, balance_amount__gt=0)

    """Completed"""
    #returns all houses with completed jobs
    def completed_houses(self):
        return House.objects.filter(customer=self.customer, completed_jobs=True)

    #returns last 50 completed jobs
    def completed_jobs(self):
        return Job.objects.filter(house__customer=self.customer, house__completed_jobs=True, approved=True, balance_amount__lte=0)[:50]

    """Current Week Results"""
    #returns all houses with payment requests for the last week
    def current_payment_requests_houses(self):
        houses = House.objects.filter(customer=self.customer)
        payments = Request_Payment.objects.filter(house__customer=self.customer, job__approved=True, approved=False)
        return self.current_week_results(houses=houses, queryset=payments, model=Request_Payment, update_field={'pending_payments': [True, False]}, approved=False, submit_date__range=[Customer.start_week, Customer.today])

    #returns all payment requests for the last week for approved jobs
    def current_payment_requests(self):
        return Request_Payment.objects.filter(job__approved=True, approved=False, submit_date__range=[Customer.start_week, Customer.today])

    """Payment History"""
    #returns all houses with a payment history for the last week
    def payment_history_houses(self):
        houses = House.objects.filter(customer=self.customer)
        payments = Request_Payment.objects.filter(house__customer=self.customer, job__approved=True, approved=True)
        return self.current_week_results(houses=houses, queryset=payments, model=Request_Payment, update_field={'payment_history': [True, False]}, approved=True, approved_date__range=[Customer.start_week, Customer.today])

    def all_payments(self):
        return Request_Payment.objects.filter(house__customer=self.customer)

    #returns all approved payments for the last week
    def current_payments(self):
        return Request_Payment.objects.filter(house__customer=self.customer, job__approved=True, approved=True, approved_date__range=[Customer.start_week, Customer.today])

    """Proposed Jobs"""
    #returns all houses with proposed jobs for the last week
    def proposed_jobs_houses(self):
        houses = House.objects.filter(customer=self.customer)
        jobs = Job.objects.filter(house__customer=self.customer, approved=False)
        return self.current_week_results(houses=houses, queryset=jobs, model=Job, update_field={'proposed_jobs': [True, False]}, approved=False, start_date__range=[Customer.start_week, Customer.today])

    #returns all proposed jobs submitted for the last week
    def proposed_jobs(self):
        return Job.objects.filter(house__customer=self.customer, approved=False, start_date__range=[Customer.start_week, Customer.today])
