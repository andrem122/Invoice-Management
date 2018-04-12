from jobs.models import Job, Current_Worker, House
from django.contrib.auth.models import User
import datetime
import pytz

class Worker:

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

    def generate_queryset(self, outer_queryset, inner_queryset):
        for o in outer_queryset:
            for i in inner_queryset:
                if getattr(o, 'address') == getattr(getattr(i, 'house'), 'address'):
                    yield o
                    break

    """Houses"""
    #gets all houses the worker is approved to work on
    def approved_houses(self):
        return Current_Worker.objects.filter(company=self.worker, current=True)

    #gets all houses the worker has pending jobs for
    def unapproved_houses(self):
        houses = House.objects.filter(customer=self.customer, proposed_jobs=True)
        jobs = Job.objects.filter(company=self.worker, approved=False, balance_amount__gt=0, start_date__range=[Worker.start_week, Worker.today])
        return self.generate_queryset(outer_queryset=houses, inner_queryset=jobs)

    #gets all houses the worker has completed jobs for
    def completed_houses(self):
        houses = House.objects.filter(customer=self.customer, completed_jobs=True)
        jobs = self.completed_jobs()
        return generate_queryset(outer_queryset=houses, inner_queryset=jobs)

    """Jobs"""
    #gets all approved jobs for the worker
    def approved_jobs(self):
        return Job.objects.filter(company=self.worker, approved=True, balance_amount__gt=0)

    #gets all unapproved jobs for the worker
    def unapproved_jobs(self):
        return Job.objects.filter(company=self.worker, approved=False, balance_amount__gt=0, start_date__range=[Worker.start_week, Worker.today])

    #gets all completed jobs for the worker
    def completed_jobs(self):
        return Job.objects.filter(company=self.worker, approved=True, balance_amount__lte=0)
