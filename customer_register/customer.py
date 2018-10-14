from jobs.models import Job, Current_Worker, House, Request_Payment
from expenses.models import Expenses
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
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    start_delta = datetime.timedelta(days=today.weekday()+6)
    start_week = today - start_delta #start week is at 5:00PM one week back

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
        self.houses = self._houses()

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
    def _houses(self, **kwargs):
        """
        Returns all houses that belong to the customer.

        Args:
            self: The object instance.

        Returns:
            A queryset of the House class.

        Raises:
            None.
        """
        return House.objects.filter(customer=self.customer, **kwargs)

    def house_totals(self, houses, **kwargs):
        """
        Gets total amount paid in jobs and expenses for each house.

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
            expenses = Expenses.objects.filter(house=house)

            #add total_paid to total for each job
            total = 0
            for job in jobs:
                total += job.total_paid

            for expense in expenses:
                total += expense.amount

            yield total

    def num_active_jobs(self, **kwargs):
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
        for house in self._houses(**kwargs):
            #get all active jobs for the each house
            yield Job.objects.filter(house=house, house__customer=self.customer, approved=True, balance_amount__gt=0).count()

    def num_completed_jobs(self, **kwargs):
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
        for house in self._houses(**kwargs):
            #get all active jobs for the each house
            yield Job.objects.filter(house=house, house__customer=self.customer, approved=True, balance_amount__lte=0).count()

    def num_expenses(self, **kwargs):
        """
        Gets the number of expenses for each house of the customer.

        Args:
            self: The object instance.

        Returns:
            A generator object with integers representing the number
            of completed jobs for each house.

        Raises:
            None.
        """
        for house in self._houses(**kwargs):
            #get all expenses for the each house
            yield Expenses.objects.filter(
                house=house,
                house__customer=self.customer,
            ).count()

    """Current (Active) Houses"""
    def active_houses(self):
        """
        Gets all active houses.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.
        """
        """compare house with active jobs to customer house.
        if the houses are the same, then it is a current customer house"""
        sql = 'SELECT * FROM jobs_current_worker WHERE current=1 GROUP BY house_id'
        all_current_workers = Current_Worker.objects.raw(sql)

        for current_worker in all_current_workers:
            if current_worker.house in self.houses:
                yield current_worker.house

    def approved_jobs(self):
        """
        Gets all approved jobs.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Job.objects.filter(house__customer=self.customer, approved=True, balance_amount__gt=0)

    """Completed"""
    def completed_houses(self):
        """
        Gets all houses with completed jobs.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.
        """
        for house in self._houses(archived=False):
            if Job.objects.filter(house=house, approved=True, balance_amount__lte=0).exists():
                yield house

    def completed_jobs(self, **kwargs):
        """
        Gets completed jobs.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Job.objects.filter(
            house__customer=self.customer,
            approved=True,
            balance_amount__lte=0,
            house__archived=False,
            **kwargs
        )

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
        return Request_Payment.objects.filter(
            house__customer=self.customer,
            job__approved=True,
            submit_date__range=[Customer.start_week, Customer.today],
            **kwargs
        )

    def current_week_payment_requests_houses(self):
        """
        Gets all houses with payment requests for the current week.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.

        Notes: House pending_payments attribute will NOT update
              if you filter houses by pending_payments=True in the queryset below
        """
        houses = House.objects.filter(customer=self.customer, pending_payments=True)
        return self.current_week_results(
            houses=houses,
            model=Request_Payment,
            update_field={'pending_payments': [True, False]},
            job__approved=True,
            approved=False,
            submit_date__range=[Customer.start_week, Customer.today]
        )

    def current_week_payment_requests(self, **kwargs):
        """
        Gets all payment requests for approved jobs for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Request_Payment.objects.filter(
            job__approved=True,
            approved=False,
            submit_date__range=[Customer.start_week, Customer.today],
            **kwargs
        )
    def current_week_payment_history_houses(self):
        """
        Gets all houses with a payment history for the current week.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.

        Notes: House payment_history attribute will NOT update
               if you filter houses by payment_history=True in the queryset below
        """
        houses = House.objects.filter(customer=self.customer, payment_history=True)
        return self.current_week_results(houses=houses, model=Request_Payment, update_field={'payment_history': [True, False]}, job__approved=True, approved=True, approved_date__range=[Customer.start_week, Customer.today])

    def current_week_approved_payments(self):
        """
        Gets all approved payments for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Request_Payment.objects.filter(
            house__customer=self.customer,
            job__approved=True,
            approved=True,
            approved_date__range=[Customer.start_week, Customer.today],
        )

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
        return Job.objects.filter(
            house__customer=self.customer,
            house__completed_jobs=True,
            approved=True,
            balance_amount__lte=0,
            start_date__range=[Customer.start_week, Customer.today],
            **kwargs
        )

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
        return self.current_week_results(
            houses=houses,
            model=Job,
            update_field={'rejected_jobs': [True, False]},
            house__customer=self.customer,
            approved=False,
            rejected=True,
            start_date__range=[Customer.start_week, Customer.today]
        )

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
        return Job.objects.filter(
            house__customer=self.customer,
            approved=False,
            rejected=True,
            start_date__range=[Customer.start_week, Customer.today],
            **kwargs
        )

    def current_week_rejected_payment_houses(self):
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
        return self.current_week_results(
            houses=houses,
            model=Request_Payment,
            update_field={'rejected_payments': [True, False]},
            house__customer=self.customer,
            job__approved=True,
            approved=False,
            rejected=True,
            submit_date__range=[Customer.start_week, Customer.today]
        )

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
        return Request_Payment.objects.filter(
            house__customer=self.customer,
            approved=False,
            rejected=True,
            submit_date__range=[Customer.start_week, Customer.today],
            **kwargs
        )

    def all_payments(self):
        """
        Gets all payments.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Request_Payment.objects.filter(house__customer=self.customer)

    """Proposed Jobs (Estimates)"""
    def proposed_jobs_houses(self):
        """
        Gets all houses with proposed jobs for the current week.

        Args:
            self: The object instance.

        Returns:
            A generator.

        Raises:
            None.
        """
        houses = House.objects.filter(customer=self.customer)
        return self.current_week_results(
            houses=houses,
            model=Job,
            update_field={'proposed_jobs': [True, False]},
            house__customer=self.customer,
            approved=False,
            rejected=False,
            start_date__range=[Customer.start_week, Customer.today],
        )

    def proposed_jobs(self, **kwargs):
        """
        Gets all proposed jobs.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Job.objects.filter(
            house__customer=self.customer,
            approved=False,
            rejected=False,
        )

    def current_week_proposed_jobs(self, **kwargs):
        """
        Gets all proposed jobs for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Job.objects.filter(
            house__customer=self.customer,
            approved=False,
            rejected=False,
            start_date__range=[Customer.start_week, Customer.today],
            **kwargs
        )

    """Expenses"""
    def expenses_houses(self):
        """
        Gets all houses with expenses.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return House.objects.filter(
            customer=self.customer,
            expenses=True,
            archived=False,
        )

    def expenses_houses_pay(self):
        """
        Gets all houses with expenses
        that have 'pay_this_week' set to true.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        houses = House.objects.filter(
            customer=self.customer,
            expenses=True
        )

        for house in houses:
            if Expenses.objects.filter(
                house=house,
                house__customer=self.customer,
                submit_date__range=[Customer.start_week, Customer.today],
                pay_this_week=True,
            ).exists():
                yield house

    def all_expenses(self):
        """
        Gets all expenses.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Expenses.objects.filter(
            customer=self.customer,
            house__archived=False,
        )

    def current_week_expenses(self, **kwargs):
        """
        Gets all expenses submitted in the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return Expenses.objects.filter(
            house__customer=self.customer,
            submit_date__range=[Customer.start_week, Customer.today],
            **kwargs
        )
