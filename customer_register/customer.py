from jobs.models import Job, Current_Worker, House, Request_Payment
from expenses.models import Expenses
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain
import datetime, pytz

class Customer:
    """
    Creates an object for customers to view jobs and houses of different status
    customer: a User object representing the customer
    houses: a queryset of all houses that belong to the customer
    """
    #filter results by the last week
    #note: add 1 day to 'today' because time seems to lag in the server
    today = datetime.datetime.now() + datetime.timedelta(days=2)
    start_delta = datetime.timedelta(days=today.weekday() + 4)
    start_week = today - start_delta #start week is one week back

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


    """Current (Active) Houses"""
    def active_houses(self):
        """
        Gets all active houses of the customer.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """

        sql = """
        SELECT h.id, h.address
        FROM jobs_house h
        INNER JOIN jobs_job j
        ON j.house_id = h.id
        WHERE customer_id = %s
        AND j.approved = 1
        AND COALESCE(j.start_amount, 0) - COALESCE(
            (SELECT COALESCE(SUM(p.amount), 0)
             FROM jobs_request_payment p
             WHERE p.job_id = j.id
             AND p.approved = 1
             AND j.approved = 1), 0)
        > 0;
        """
        return House.objects.raw(sql, params=[self.customer.id])

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
        return Job.objects.add_balance().filter(
            house__customer=self.customer,
            approved=True,
            balance1__gt=0,
        )

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
        sql = """
        SELECT DISTINCT h.id, h.address
        FROM jobs_house h
        INNER JOIN jobs_job j
        ON j.house_id = h.id
        WHERE customer_id = %s
        AND j.approved = 1
        AND COALESCE(j.start_amount, 0) - COALESCE(
            (SELECT COALESCE(SUM(p.amount), 0)
             FROM jobs_request_payment p
             WHERE p.job_id = j.id
             AND p.approved = 1
             AND j.approved = 1), 0)
        <= 0;
        """
        return House.objects.raw(sql, params=[self.customer.id])

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
        return Job.objects.add_balance().filter(
            house__customer=self.customer,
            approved=True,
            balance1__lte=0,
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
            A queryset.

        Raises:
            None.
        """

        return Request_Payment.objects.filter(
            Q(house__customer=self.customer),
            Q(job__approved=True),
            Q(submit_date__range=[Customer.start_week, Customer.today]) | Q(approved_date__range=[Customer.start_week, Customer.today]),
            **kwargs
        )

        """
        SELECT u.id, u.username,

        COALESCE((SELECT SUM(r.amount)
        FROM jobs_request_payment r
        INNER JOIN jobs_job j
        ON r.job_id = j.id
        WHERE j.approved = 1
        AND r.approved = 1
        AND j.company_id = u.id), 0)
        AS total_paid

        FROM auth_user u;
        """


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

    def current_week_new_payment_requests(self, **kwargs):
        """
        Gets all new payment requests for approved jobs that have not been
        rejected or approved for the current week.

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
            rejected=False,
            submit_date__range=[Customer.start_week, Customer.today],
            **kwargs
        )

    def current_week_approved_payments(self, **kwargs):
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
            **kwargs
        )

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
        return Job.objects.add_balance().filter(
            house__customer=self.customer,
            approved=True,
            balance1__lte=0,
            start_date__range=[Customer.start_week, Customer.today],
            **kwargs
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
        return House.objects.filter(
            customer=self.customer,
            expense_house__submit_date__range=[Customer.start_week, Customer.today],
            expense_house__pay_this_week=True,
        ).distinct()

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

    """Houses"""
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
        return House.objects.filter(customer=self.customer, **kwargs).order_by('address')

    """Current Week Houses"""
    def current_week_payment_requests_houses(self):
        """
        Gets all houses with payment requests for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.

        Notes: House pending_payments attribute will NOT update
              if you filter houses by pending_payments=True in the queryset below
        """
        return House.objects.filter(
            customer=self.customer,
            job__approved=True,
            request_payment__approved=False,
            request_payment__submit_date__range=[Customer.start_week, Customer.today],
        ).distinct()

    def current_week_payment_history_houses(self):
        """
        Gets all houses with a payment history for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.

        Notes: House payment_history attribute will NOT update
               if you filter houses by payment_history=True in the queryset below
        """
        return House.objects.filter(
            customer=self.customer,
            job__approved=True,
            request_payment__approved=True,
            request_payment__approved_date__range=[Customer.start_week, Customer.today],
        ).distinct()

    def current_week_completed_houses(self):
        """
        Gets houses with completed jobs for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """

        sql = """
        SELECT DISTINCT h.id, h.address
        FROM jobs_house h
        INNER JOIN jobs_job j
        ON j.house_id = h.id
        WHERE customer_id = %s
        AND j.approved = 1
        AND j.start_date BETWEEN %s AND %s
        AND COALESCE(j.start_amount, 0) - COALESCE(
            (SELECT COALESCE(SUM(p.amount), 0)
             FROM jobs_request_payment p
             WHERE p.job_id = j.id
             AND p.approved = 1
             AND j.approved = 1), 0)
        <= 0;
        """
        return House.objects.raw(sql, params=[self.customer.id, Customer.start_week, Customer.today])

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
        return House.objects.filter(
            customer=self.customer,
            job__approved=False,
            job__rejected=True,
            job__start_date__range=[Customer.start_week, Customer.today],
        ).distinct()

    def current_week_rejected_payment_houses(self):
        """
        Gets all houses with rejected payments for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return House.objects.filter(
            customer=self.customer,
            job__approved=True,
            request_payment__approved=False,
            request_payment__rejected=True,
            request_payment__submit_date__range=[Customer.start_week, Customer.today],
        ).distinct()

    def current_week_proposed_jobs_houses(self):
        """
        Gets all houses with proposed jobs for the current week.

        Args:
            self: The object instance.

        Returns:
            A queryset.

        Raises:
            None.
        """
        return House.objects.filter(
            customer=self.customer,
            job__approved=False,
            job__rejected=False,
            job__start_date__range=[Customer.start_week, Customer.today],
        ).distinct()
