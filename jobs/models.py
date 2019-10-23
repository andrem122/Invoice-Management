from django.db import models
from django.conf import settings
from django.db.models.functions import Coalesce
from django.db.models.expressions import RawSQL
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, IntegerField, Func, Subquery, OuterRef
import os

#create database table structure here
class Round(Func):
  function = 'ROUND'
  arity = 2

class House_Set(models.QuerySet):

    def add_total_spent(self):
        from expenses.models import Expenses

        return self.annotate(
            total_spent=Coalesce(
                Subquery(
                    Request_Payment.objects
                    .filter(
                        house_id=OuterRef('pk'),
                        approved=True
                    ).values('house_id')
                    .order_by()
                    .annotate(
                        sum=Sum('amount')
                    ).values('sum')[:1],
                    output_field=DecimalField()
                ), 0) +
                Coalesce(
                    Subquery(
                        Expenses.objects
                        .filter(
                            house_id=OuterRef('pk')
                        ).values('house_id')
                        .order_by()
                        .annotate(
                            sum=Sum('amount')
                        ).values('sum')[:1],
                        output_field=DecimalField()
                ), 0)
        )

    def add_budget(self):
        return self.annotate(
            budget=ExpressionWrapper(
                Round(0.933 * F('after_repair_value') - F('purchase_price') - F('profit') - 400.00, 2),
                output_field=DecimalField()
            )
        )

    def add_budget_balance(self):
        return self.add_budget().add_total_spent().annotate(
            budget_balance=ExpressionWrapper(
                F('budget') - F('total_spent'),
                output_field=DecimalField()
            ),
            budget_balance_degree=ExpressionWrapper(
                Round(360 * F('total_spent') / F('budget'), 4),
                output_field=DecimalField()
            )
        )

    def add_percent_budget_used(self):
        return self.add_budget().add_total_spent().annotate(
            percent_budget_used=ExpressionWrapper(
                F('total_spent') / F('budget'),
                output_field=IntegerField()
            )
        )

    def add_potential_profit(self):
        return self.add_total_spent().annotate(
            potential_profit=ExpressionWrapper(
                Round(0.933 * F('after_repair_value') - F('purchase_price') - F('total_spent') - 400.00, 2),
                output_field=DecimalField()
            )
        )

    def add_num_approved_jobs(self):
        return self.annotate(
            num_approved_jobs=Coalesce(
                Subquery(
                    Job.objects
                    .filter(
                        house_id=OuterRef('pk'),
                        approved=True,
                    ).values('house_id')
                    .order_by()
                    .annotate(
                        count=Count('pk')
                    ).values('count')[:1],
                    output_field=IntegerField()
            ), 0)
        )

    def add_num_active_jobs(self):
        sql = """
        COALESCE(
        (SELECT COUNT(U0.id)
        FROM jobs_job U0
        WHERE (U0.approved = TRUE AND U0.house_id = (jobs_house.id))
        AND COALESCE(U0.start_amount, 0) - COALESCE((SELECT SUM(p.amount)
            FROM jobs_request_payment p
            WHERE p.job_id = U0.id
            AND U0.approved = TRUE
            AND p.approved = TRUE
            GROUP BY U0.id), 0) > 0
        GROUP BY U0.house_id
        LIMIT 1), 0)
        """

        return self.annotate(
            num_active_jobs=RawSQL(sql, params=())
        )

    def add_num_expenses(self):
        from expenses.models import Expenses
        return self.annotate(
            num_expenses=Coalesce(
                Subquery(
                    Expenses.objects
                    .filter(
                        house_id=OuterRef('pk'),
                    ).values('house_id')
                    .order_by()
                    .annotate(
                        count=Count('pk')
                    ).values('count')[:1],
                    output_field=IntegerField()
            ), 0)
        )

class House(models.Model):
    address = models.CharField(max_length=250)
    companies = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_house')
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    after_repair_value = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    #jobs
    proposed_jobs = models.BooleanField(default=False)
    completed_jobs = models.BooleanField(default=False)
    rejected_jobs = models.BooleanField(default=False)

    #payments
    payment_history = models.BooleanField(default=False)
    pending_payments = models.BooleanField(default=False)
    rejected_payments = models.BooleanField(default=False)

    expenses = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    objects = House_Set.as_manager()

    def __str__(self):
        return self.address


    def generate_file_path(self, file_name):
        return os.path.join('customer_uploads', 'add_house', str(file_name))

    house_list_file = models.FileField(null=True, blank=False)

class Job_Set(models.QuerySet):
    def add_total_paid(self):
        return self.annotate(
            total_paid1=Coalesce(
                Subquery(
                    Request_Payment.objects
                    .filter(
                        job_id=OuterRef('pk'),
                        approved=True
                    ).values('job_id')
                    .order_by()
                    .annotate(
                        sum=Sum('amount')
                    ).values('sum')[:1],
                    output_field=DecimalField()
                ), 0)
        )

    def add_balance(self):
        return self.add_total_paid().annotate(
            balance1=ExpressionWrapper(
                F('start_amount') - F('total_paid1'),
                output_field=DecimalField()
            )
        )

class Job(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=True)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    start_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    notes = models.TextField(max_length=3000, default='No notes...')
    objects = Job_Set.as_manager()

    #categories
    electric = 'Electric'
    plumbing = 'Plumbing'
    drywall = 'Drywall'
    roofing = 'Roofing'
    window_door = 'Window/Door'
    demolition = 'Demolition'
    landscaping = 'Landscaping'
    cabinets_countertops = 'Cabinet/Countertop'
    misc = 'Miscellaneous'

    job_choices = (
        ('', 'Job Type'),
        (electric, 'Electric'),
        (plumbing, 'Plumbing'),
        (drywall, 'Drywall'),
        (roofing, 'Roofing'),
        (window_door, 'Window/Door'),
        (demolition, 'Demolition'),
        (landscaping, 'Landscaping'),
        (cabinets_countertops, 'Cabinet/Countertop'),
        (misc, 'Miscellaneous'),
    )

    job_type = models.CharField(max_length=100, choices=job_choices, default='', blank=True)

    def __str__(self):
        return str(self.company.get_username()) + '-' + str(self.house.address + '-' + str(self.start_amount))

    def generate_file_path(self, file_name):
        return os.path.join('worker_uploads', str(self.house.address), str(file_name))

    document_link = models.FileField(null=True, blank=True, upload_to=generate_file_path)

    #balance is calculated using start_amount and total_paid
    @property
    def balance(self):
        return float(self.start_amount) - float(self.total_paid)

    balance_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class Request_Payment(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True, blank=True)
    approved_date = models.DateTimeField(auto_now_add=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    created_by_system = models.BooleanField(default=False)

    def __str__(self):
        info = [self.job.id, self.house.address, self.job.company, self.amount, self.approved]
        info = [str(x) for x in info]

        return info[0] + '-' + info[1] + '-' + info[2] + '-' + info[3] + info[4]

    def generate_file_path_worker(self, file_name):
        return os.path.join('worker_uploads', str(self.house.address), str(file_name))

    def generate_file_path_customer(self, file_name):
        return os.path.join('customer_uploads', 'documents', str(self.house.address), str(file_name))


    document_link = models.FileField(null=True, upload_to=generate_file_path_worker)
    paid_link = models.FileField(null=True, upload_to=generate_file_path_customer)
