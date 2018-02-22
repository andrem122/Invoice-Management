from jobs.models import Job, Current_Worker, House, Request_Payment
import datetime
import pytz

class Customer():
    utc = pytz.UTC
    #filter results by 2 weeks
    date = datetime.datetime.now()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(14)

    start_week = start_week.replace(tzinfo=utc)
    end_week = end_week.replace(tzinfo=utc)

    def __init__(self, customer):
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
        result_queryset = []
        #house object
        for h in houses:
            #current house object
            for q in queryset.iterator():
                #get attributes to compare
                #{0: 0}, {1: 'house'}
                a = self.attribute_level(obj=h, compare=compare[0])
                b = self.attribute_level(obj=q, compare=compare[1])
                if a == b:
                    if append_outer == True:
                        result_queryset.append(h)
                    else:
                        result_queryset.append(q)

        return result_queryset

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
        #return self.get_queryset(houses=self.current_houses, queryset=approved_jobs, compare=[{1: 'house'}, {1: 'house'}])

    """Completed"""
    #returns all houses with completed jobs
    def completed_houses(self):
        return House.objects.filter(customer=self.customer, completed_jobs=True)

    #return all completed jobs
    def completed_jobs(self):
        return Job.objects.filter(house__customer=self.customer, house__completed_jobs=True, approved=True, balance_amount__lte=0)
        #return self.get_queryset(houses=self.completed_houses, queryset=completed_jobs, compare=[{0: 0}, {1: 'house'}])

    """Current 2 Weeks Results"""
    #returns current(2 weeks) payment requests for approved jobs
    def current_payment_requests(self):
        return Request_Payment.objects.filter(job__approved=True, approved=False, submit_date__range=[Customer.start_week, Customer.end_week])

    """Payment History"""
    #returns all houses with a payment history for the last 2 weeks
    def payment_history_houses(self):
        return House.objects.filter(customer=self.customer, payment_history=True)

    #returns all approved payments for the last 2 weeks
    def current_payments(self):
        return Request_Payment.objects.filter(approved=True, approved_date__range=[Customer.start_week, Customer.end_week])

    """Proposed Jobs"""
    #returns all houses with proposed jobs
    def proposed_jobs_houses(self):
        return House.objects.filter(customer=self.customer, proposed_jobs=True)

    #returns all proposed jobs submitted within the last 2 weeks
    def proposed_jobs(self):
        return Job.objects.filter(house__customer=self.customer, approved=False, start_date__range=[Customer.start_week, Customer.end_week])
