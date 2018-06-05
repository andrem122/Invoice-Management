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

    def current_week_results(self, houses, model, update_field={}, **kwargs):
        """
        Fetches current week results, if there are none
        then set the appropriate house attributes to false

        Args:
            self: The object instance.
            houses: A queryset of the House class.
            model: A model class.
            update_field: A dictionary representing the attributes
            of the model class.

        Returns:
            A generator object consisting of House objects of the customer.

        Raises:
            None.
        """
        for house in houses.iterator():
            if model.objects.filter(house=house, **kwargs).exists():
                setattr(house, list(update_field.keys())[0], list(update_field.values())[0][0])
                house.save(update_fields=[list(update_field.keys())[0]])
                yield house
            else:
                setattr(house, list(update_field.keys())[0], list(update_field.values())[0][1])
                house.save(update_fields=[list(update_field.keys())[0]])

    """Attributes of Houses"""
    def houses(self):
        """
        Returns all houses that belong to the customer.

        Args:
            self: The object instance.

        Returns:
            A queryset of the House class.

        Raises:
            None.
        """
        return House.objects.filter(customer=self.customer)

    def house_totals(self, houses, **kwargs):
        """
        Gets total amount paid for each house.

        Args:
            self: The object instance.
            houses: Queryset of the House class.

        Returns:
            The total amount spent as a float type.

        Raises:
            None.
        """
        for house in houses:
            #get all jobs for the current house
            jobs = Job.objects.filter(house=house, **kwargs)

            #add total_paid to total for each job
            total = 0
            for job in jobs:
                total += job.total_paid

            yield total

    def num_active_jobs(self):
        """
        Gets the number of active jobs for each house of the customer.

        Args:
            self: The object instance.

        Returns:
            A generator object with integers representing the number
            of active jobs for each house.

        Raises:
            None.
        """
        for house in self.houses:
            #get all active jobs for the each house
            yield Job.objects.filter(house=house, house__customer=self.customer, approved=True, balance_amount__gt=0).count()

    def num_completed_jobs(self):
        """
        Gets the number of completed jobs for each house of the customer.

        Args:
            self: The object instance.

        Returns:
            A generator object with integers representing the number
            of completed jobs for each house.

        Raises:
            None.
        """
        for house in self.houses:
            #get all active jobs for the each house
            yield Job.objects.filter(house=house, house__customer=self.customer, approved=True, balance_amount__lte=0).count()

    """Current(Active) Houses"""
    #returns houses that are activley being worked on by workers
    def active_houses(self):
        """compare house with active jobs to customer house.
        if the houses are the same, then it is a current customer house"""
        sql = 'SELECT * FROM jobs_current_worker WHERE current=1 GROUP BY house_id'
        all_current_workers = Current_Worker.objects.raw(sql)

        for current_worker in all_current_workers:
            if current_worker.house in self.houses:
                yield current_worker.house

    #returns all approved jobs for houses for each customer
    def approved_jobs(self):
        return Job.objects.filter(house__customer=self.customer, approved=True, balance_amount__gt=0)

    """Completed"""
    #returns all houses with completed jobs
    def completed_houses(self):
        return House.objects.filter(customer=self.customer, completed_jobs=True)

    #returns completed jobs
    def completed_jobs(self, **kwargs):
        return Job.objects.filter(house__customer=self.customer, house__completed_jobs=True, approved=True, balance_amount__lte=0, **kwargs)

    """Current Week Results"""
    def current_week_payments_all(self, **kwargs):
        """
        Gets all payments for the current week.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.
        """
        return Request_Payment.objects.filter(house__customer=self.customer, job__approved=True, submit_date__range=[Customer.start_week, Customer.today], **kwargs)

    #returns all houses with payment requests for the last week
    def current_payment_requests_houses(self):
        """
        Note: House pending_payments attribute will NOT update
        if you filter houses by pending_payments=True in the queryset below
        """
        houses = House.objects.filter(customer=self.customer, pending_payments=True)
        return self.current_week_results(houses=houses, model=Request_Payment, update_field={'pending_payments': [True, False]}, job__approved=True, approved=False, submit_date__range=[Customer.start_week, Customer.today])

    #returns all payment requests for the last week for approved jobs
    def current_payment_requests(self, **kwargs):
        return Request_Payment.objects.filter(job__approved=True, approved=False, submit_date__range=[Customer.start_week, Customer.today], **kwargs)

    def current_week_completed_houses(self):
        """
        Gets completed houses for the current week.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.
        """
        houses = House.objects.filter(customer=self.customer, completed_jobs=True)
        return self.current_week_results(houses=houses, model=Job, update_field={'completed_jobs': [True, False]}, house__customer=self.customer, house__completed_jobs=True, approved=True, balance_amount__lte=0, start_date__range=[Customer.start_week, Customer.today])

    def current_week_completed_jobs(self, **kwargs):
        """
        Gets completed jobs for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Job.objects.filter(house__customer=self.customer, house__completed_jobs=True, approved=True, balance_amount__lte=0, start_date__range=[Customer.start_week, Customer.today], **kwargs)

    def current_week_rejected_job_houses(self):
        """
        Gets houses with rejected jobs for the current week.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.
        """
        houses = House.objects.filter(customer=self.customer, rejected_jobs=True)
        return self.current_week_results(houses=houses, model=Job, update_field={'rejected_jobs': [True, False]}, house__customer=self.customer, approved=False, rejected=True, start_date__range=[Customer.start_week, Customer.today])

    def current_week_rejected_jobs(self, **kwargs):
        """
        Gets rejected jobs for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Job.objects.filter(house__customer=self.customer, approved=False, rejected=True, start_date__range=[Customer.start_week, Customer.today], **kwargs)

    def current_week_rejected_job_houses(self):
        """
        Gets houses with rejected payments for the current week.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.
        """
        houses = House.objects.filter(customer=self.customer, rejected_payments=True)
        return self.current_week_results(houses=houses, model=Job, update_field={'rejected_jobs': [True, False]}, house__customer=self.customer, approved=False, rejected=True, start_date__range=[Customer.start_week, Customer.today])

    def current_week_rejected_payments_houses(self):
        """
        Gets all houses with rejected payments for the current week.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.
        """
        houses = House.objects.filter(customer=self.customer, rejected_payments=True)
        return self.current_week_results(houses=houses, model=Request_Payment, update_field={'rejected_payments': [True, False]}, house__customer=self.customer, approved=False, rejected=True, submit_date__range=[Customer.start_week, Customer.today])

    def current_week_rejected_payments(self, **kwargs):
        """
        Gets rejected payments for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Request_Payment.objects.filter(house__customer=self.customer, approved=False, rejected=True, submit_date__range=[Customer.start_week, Customer.today], **kwargs)

    """Payments"""
    #returns all houses with a payment history for the last week
    def payment_history_houses(self):
        """
        Note: House payment_history attribute will NOT update
        if you filter houses by payment_history=True in the queryset below
        """
        houses = House.objects.filter(customer=self.customer, payment_history=True)
        return self.current_week_results(houses=houses, model=Request_Payment, update_field={'payment_history': [True, False]}, job__approved=True, approved=True, approved_date__range=[Customer.start_week, Customer.today])

    def all_payments(self):
        return Request_Payment.objects.filter(house__customer=self.customer)

    #returns all approved payments for the last week
    def current_payments(self):
        return Request_Payment.objects.filter(house__customer=self.customer, job__approved=True, approved=True, approved_date__range=[Customer.start_week, Customer.today])

    """Proposed Jobs"""
    #returns all houses with proposed jobs for the last week
    def proposed_jobs_houses(self):
        houses = House.objects.filter(customer=self.customer, proposed_jobs=True)
        return self.current_week_results(houses=houses, model=Job, update_field={'proposed_jobs': [True, False]}, approved=False, rejected=False, start_date__range=[Customer.start_week, Customer.today])

    #returns all proposed jobs submitted for the last week
    def proposed_jobs(self, **kwargs):
        return Job.objects.filter(house__customer=self.customer, approved=False, rejected=False, start_date__range=[Customer.start_week, Customer.today], **kwargs)
