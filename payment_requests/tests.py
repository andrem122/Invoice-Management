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

        #create test data
        self.house = House.objects.create(id=1, address='1234 N Test Way', customer=self.customer)
        self.job = Job.objects.create(id=1,
            house=self.house,
            company=self.worker,
            start_amount=5000.00,
            balance_amount=1000.00,
            total_paid=4000.00,
            document_link='worker_uploads/house/file.ext',
            approved=True,
        )
        self.payment = Request_Payment.objects.create(id=1, house=self.house, job=self.job, amount=4000.00, requested_by_worker=True)
    def test_approved_payments_get(self):
        response = self.c.get('/payment_requests/approved_payments')
        self.assertEqual(response.status_code, 200)
    def test_approved_payments_post(self):
        response = self.c.post('/payment_requests/approved_payments', {'job_id': '1', 'p_id': '1'})
        #check if values are correct
        self.assertTrue(House.objects.get(pk=1).pending_payments)

        self.assertEqual(Job.objects.get(pk=1).balance_amount, 5000.00)
        self.assertEqual(Job.objects.get(pk=1).total_paid, 0.00)
        self.assertTrue(Job.objects.get(pk=1).approved)

        self.assertEqual(Request_Payment.objects.get(pk=1).approved, False)

        self.assertIsNotNone(Current_Worker.objects.get(pk=1))
        self.assertRedirects(response, '/payment_requests/approved_payments')
