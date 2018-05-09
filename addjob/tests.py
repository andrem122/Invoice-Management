from django.test import TestCase
from django.test import Client
from .views import add_job
from django.contrib.auth.models import User, Group
from jobs.models import Job, House, Request_Payment

class Test_Payment_Requests(TestCase):
    def setUp(self):
        #create groups
        customer_group = Group.objects.get_or_create(name='Customers')[0]
        customer_id_group = Group.objects.get_or_create(name='1')[0]
        worker_group = Group.objects.get_or_create(name='Workers')[0]

        #create users
        self.customer = User.objects.get_or_create(username='customer')[0]
        self.customer.groups.add(customer_group)
        self.worker = User.objects.get_or_create(username='worker')[0]
        self.worker.groups.add(worker_group)
        self.worker.groups.add(customer_id_group)

        #create client and log customer in
        self.c = Client()
        self.c.force_login(self.worker)
    def test_addjob_get(self):
        """Test GET request on addjob view"""
        response = self.c.get('/addjob')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, '/addjob/')
    def test_addjob_post(self):
        """Test POST request to add job"""
        #create test data
        house = House.objects.create(
            pk=1,
            address='1234 N Test Way',
            customer=self.customer,
            completed_jobs=False,
            payment_history=False,
            proposed_jobs=False,
            pending_payments=False,
        )

        house.save()

        #POST data with file upload
        with open('/home/andre/Downloads/show.pdf', 'rb') as f:
            response = self.c.post(
                '/addjob/',
                {'house': 1, 'start_amount': '5000.00', 'document_link': f}
            )

        #check if values are correct after POST request
        house = House.objects.get(pk=1)
        self.assertFalse(house.completed_jobs)
        self.assertFalse(house.payment_history)
        self.assertTrue(house.proposed_jobs)
        self.assertFalse(house.pending_payments)

        job = Job.objects.get(pk=1)
        self.assertequal(Job.objects.count(), 1)
        self.assertEqual(float(job.balance_amount), 5000.00)
        self.assertEqual(float(job.start_amount), 5000.00)
        self.assertEqual(float(job.total_paid), 0.00)
        self.assertFalse(job.approved)
        self.assertEqual(job.house, house)
        self.assertEqual(job.document_link, 'worker_uploads/1234 N Test Way/show.pdf')
        self.assertEqual(job.company, self.worker)
        self.assertFalse(job.rejected)
