from jobs.models import Job, House
from django.contrib.auth.models import User
import datetime
import pytz

class Worker:
    """
    Creates an object for workers to view jobs and houses of different status
    worker: a User object representing the worker
    customer: a User object representing the customer that the worker belongs to
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

    def __init__(self, worker):
        self.worker = worker

        #get customer object associated with the worker
        customer_id = worker.groups.values_list('name', flat=True)[1]
        if customer_id == 'Workers':
            customer_id = worker.groups.values_list('name', flat=True)[0]
        customer_id = int(customer_id)
        self.customer = User.objects.get(pk=customer_id)

    """Houses"""
    #gets all houses the worker is approved to work on
    def current_week_approved_houses(self):
        return House.objects.filter(
            customer=self.customer,
            job__company=self.worker,
            job__approved=True,
            job__rejected=False,
            job__start_date__range=[Worker.start_week, Worker.today],
        )

    #get all houses with pending jobs for the current week
    def current_week_unapproved_houses(self):
        return House.objects.filter(
            customer=self.customer,
            job__company=self.worker,
            job__approved=False,
            job__rejected=False,
            job__start_date__range=[Worker.start_week, Worker.today],
        )

    #gets all houses the worker has completed jobs for the current week
    def current_week_completed_houses(self):
        sql = """
        SELECT DISTINCT h.id, h.address
        FROM jobs_house h
        INNER JOIN jobs_job j
        ON j.house_id = h.id
        WHERE customer_id = %s
        AND j.company_id = %s
        AND j.approved = TRUE
        AND j.start_date BETWEEN %s AND %s
        AND COALESCE(j.start_amount, 0) - COALESCE(
            (SELECT COALESCE(SUM(p.amount), 0)
             FROM jobs_request_payment p
             WHERE p.job_id = j.id
             AND p.approved = TRUE
             AND j.approved = TRUE), 0)
        <= 0;
        """
        return House.objects.raw(sql, params=[self.customer.id, self.worker.id, Worker.start_week, Worker.today])

    """Jobs"""
    #gets all approved jobs for the worker
    def active_jobs(self):
        return Job.objects.add_balance().filter(
            company=self.worker,
            approved=True,
            balance1__gt=0,
        )

    #gets all unapproved jobs for the worker for the current week
    def current_week_unapproved_jobs(self):
        return Job.objects.add_balance().filter(
            company=self.worker,
            approved=False,
            rejected=False,
            balance1__gt=0,
            start_date__range=[Worker.start_week, Worker.today],
        )

    #gets all completed jobs for the worker for the current week
    def current_week_completed_jobs(self):
        return Job.objects.add_balance().filter(
            company=self.worker,
            approved=True,
            balance1__lte=0,
            start_date__range=[Worker.start_week, Worker.today],
        )
