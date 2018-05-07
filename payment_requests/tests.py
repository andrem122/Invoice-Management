from django.test import TestCase
from django.test import Client
from .views import approved_payments
from django.conf import settings
from django.contrib.auth.models import User, Group
from jobs.models import Job, House, Request_Payment, Current_Worker
import datetime

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
    def test_approved_payments_get(self):
        response = self.c.get('/payment_requests/approved_payments')
        self.assertEqual(response.status_code, 200)
    def test_approved_payments_by_worker(self):
        """
        Test if values for house, job, payment, and current_worker
        are correct after unapproving a payment for a house that originally
        had 1 completed job, had 1 approved payment, had 0
        pending payments, had 0 proposed_jobs, and payment with
        attribute requested_by_worker=True
        """
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
            balance_amount=1000.00,
            total_paid=4000.00,
            document_link='worker_uploads/house/file.ext',
            approved=True,
        )
        payment = Request_Payment.objects.create(
            pk=1,
            house=house,
            job=job,
            amount=4000.00,
            requested_by_worker=True,
            approved=True,
        )

        house.save()
        job.save()
        payment.save()

        response = self.c.post('/payment_requests/approved_payments', {'job_id': '1', 'p_id': '1'})
        #check if values are correct after POST request
        house = House.objects.get(pk=1)
        self.assertTrue(house.pending_payments)
        self.assertFalse(house.completed_jobs)
        self.assertFalse(house.payment_history)
        self.assertFalse(house.proposed_jobs)

        job = Job.objects.get(pk=1)
        self.assertEqual(float(job.balance_amount), 5000.00)
        self.assertEqual(float(job.start_amount), 5000.00)
        self.assertEqual(float(job.total_paid), 0.00)
        self.assertTrue(job.approved)
        self.assertEqual(job.house, house)
        self.assertEqual(job.document_link, 'worker_uploads/house/file.ext')
        self.assertEqual(job.company, self.worker)

        payment = Request_Payment.objects.get(pk=1)
        self.assertFalse(payment.approved)
        self.assertTrue(payment.requested_by_worker)
        self.assertEqual(float(payment.amount), 4000.00)
        self.assertEqual(payment.job, job)
        self.assertEqual(payment.house, house)

        worker = Current_Worker.objects.get(pk=1)
        self.assertIsNotNone(worker)
        self.assertEqual(worker.company, job.company)
        self.assertTrue(worker.current)

        #check redirection after POST request is successful
        self.assertRedirects(response, '/payment_requests/approved_payments')

    def test_approved_payments_by_code(self):
        """
        Test if values for house, job, payment, and current_worker
        are correct after unapproving a payment for a house that originally
        had 1 completed job, had 1 approved payment, had 0
        pending payments, had 0 proposed_jobs, and payment with
        attribute requested_by_worker=False
        """
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
            start_amount=7354.43,
            balance_amount=0.00,
            total_paid=7354.43,
            document_link='worker_uploads/house/file.ext',
            approved=True,
        )
        payment = Request_Payment.objects.create(
            pk=1,
            house=house,
            job=job,
            amount=7354.43,
            requested_by_worker=False,
            approved=True,
        )

        house.save()
        job.save()
        payment.save()

        response = self.c.post('/payment_requests/approved_payments', {'job_id': '1', 'p_id': '1'})
        #check if values are correct after POST request
        house = House.objects.get(pk=1)
        self.assertFalse(house.pending_payments)
        self.assertFalse(house.completed_jobs)
        self.assertFalse(house.payment_history)
        self.assertTrue(house.proposed_jobs)

        job = Job.objects.get(pk=1)
        self.assertEqual(float(job.balance_amount), 7354.43)
        self.assertEqual(float(job.start_amount), 7354.43)
        self.assertEqual(float(job.total_paid), 0.00)
        self.assertFalse(job.approved)
        self.assertEqual(job.house, house)
        self.assertEqual(job.document_link, 'worker_uploads/house/file.ext')
        self.assertEqual(job.company, self.worker)

        payment = Request_Payment.objects.filter(pk=1).exists()
        self.assertFalse(payment)

        worker = Current_Worker.objects.filter(pk=1)
        self.assertFalse(worker)

        #check redirection after POST request is successful
        self.assertRedirects(response, '/payment_requests/approved_payments')
