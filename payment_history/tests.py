from django.test import TestCase
from django.test import Client
from jobs.models import House, Job, Request_Payment
from .views import p_history_job
from django.contrib.auth.models import User, Group

class Test_Payment_Requests(TestCase):
    def setUp(self):
        #create groups
        customer_group = Group.objects.get_or_create(name='Customers')[0]
        worker_group = Group.objects.get_or_create(name='Workers')[0]

        #create users
        self.customer = User.objects.get_or_create(username='customer', )[0]
        self.customer.groups.add(customer_group)
        self.worker = User.objects.get_or_create(username='worker', )[0]
        self.worker.groups.add(worker_group)

        #create client and log customer in
        self.c = Client()
        self.c.force_login(self.customer)
    def check_queryset(self, instance, attributes=(), asserts=()):
        """eliminates repetition of comparison code"""
        try:
            for attribute, assert_type in zip(attributes, asserts):
                if assert_type[0] == 'assertEqual':
                    self.assertEqual(getattr(instance, attribute), assert_type[1])
                elif assert_type[0] == 'assertTrue':
                    self.assertTrue(getattr(instance, attribute))
        except TypeError as e:
            print(e)
    def test_payment_history_get(self):
        response = self.c.get('/payment_history/p_history_job')
        self.assertEqual(response.status_code, 200)
    def test_payment_history_post(self):
        #create test data
        house = House.objects.create(
            pk=1,
            address='1234 N Test Way',
            customer=self.customer,
            completed_jobs=True,
            payment_history=True,
            proposed_jobs=False,
            pending_payments=False,
        )
        job = Job.objects.create(
            pk=1,
            house=house,
            company=self.worker,
            start_amount=5000.00,
            balance_amount=0.00,
            total_paid=5000.00,
            document_link='worker_uploads/house/file.ext',
            approved=True,
            rejected=False,
        )
        Request_Payment.objects.create(
            pk=1,
            house=house,
            job=job,
            amount=4000.00,
            requested_by_worker=True,
            approved=True,
        ).save()
        Request_Payment.objects.create(
            pk=2,
            house=house,
            job=job,
            amount=1000.00,
            requested_by_worker=True,
            approved=True,
        ).save()

        house.save()
        job.save()

        response = self.c.post(
            '/payment_history/p_history_job',
            {'view-payment-history': 'view-payment-history', 'job_house': '1234 N Test Way', 'job_id': '1'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['address'], '1234 N Test Way')
        self.assertEqual(response.context['job_id'], 1)

        payment_1 = response.context['payments'][0]
        payment_2 = response.context['payments'][1]

        attributes = ('house', 'job', 'amount', 'requested_by_worker', 'approved')
        asserts = (
            ['assertEqual', house],
            ['assertEqual', job],
            ['assertEqual', 4000.00],
            ['assertTrue', True],
            ['assertTrue', True],
        )

        self.check_queryset(instance=payment_1, attributes=attributes, asserts=asserts)
        asserts[2][1] = 1000.00
        self.check_queryset(instance=payment_2, attributes=attributes, asserts=asserts)
