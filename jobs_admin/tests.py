from django.test import TestCase
from django.test import Client
from jobs.models import Current_Worker, House, Job, Request_Payment
from .views import index
from django.contrib.auth.models import User, Group

class Test_Send_Data(TestCase):
    def setUp(self):
        #create groups
        customer_group = Group.objects.get_or_create(name='Customers')[0]
        worker_group = Group.objects.get_or_create(name='Workers')[0]

        #create users
        self.customer = User.objects.get_or_create(username='customer', )[0]
        self.customer.email = 'am3141@live.com'
        self.customer.groups.add(customer_group)
        self.worker = User.objects.get_or_create(username='worker', )[0]
        self.worker.groups.add(worker_group)

        #create client and log customer in
        self.c = Client()
        self.c.force_login(self.customer)
    def test_jobs_admin_get(self):
        response = self.c.get('/jobs_admin/')
        self.assertEqual(response.status_code, 200)
    def test_jobs_admin_post(self):
        #create test data
        House.objects.create(
            pk=1,
            address='1234 N Test Way',
            customer=self.customer,
            completed_jobs=False,
            payment_history=False,
            proposed_jobs=True,
            pending_payments=False,
        ).save()

        Job.objects.create(
            pk=1,
            house=House.objects.get(pk=1),
            company=self.worker,
            start_amount=5000.00,
            balance_amount=5000.00,
            total_paid=0.00,
            document_link='/worker_uploads/test2/pdf-sample.pdf',
            approved=False,
            rejected=False,
        ).save()

        Job.objects.create(
            pk=2,
            house=House.objects.get(pk=1),
            company=self.worker,
            start_amount=6080.00,
            balance_amount=6080.00,
            total_paid=0.00,
            document_link='/worker_uploads/test2/pdf-sample.pdf-2',
            approved=False,
            rejected=False,
        ).save()

        Job.objects.create(
            pk=3,
            house=House.objects.get(pk=1),
            company=self.worker,
            start_amount=7567.00,
            balance_amount=7567.00,
            total_paid=0.00,
            document_link='/worker_uploads/test2/pdf-sample.pdf-3',
            approved=False,
            rejected=False,
        ).save()

        #approve as payment POST
        response = self.c.post(
            '/jobs_admin/',
            {
                'job_id': 1,
                'approve-as-payment': 'approve-as-payment',
            }
        )

        #current worker
        self.assertEqual(Current_Worker.objects.count(), 0)

        #house
        house = House.objects.get(pk=1)
        self.assertTrue(house.completed_jobs)
        self.assertTrue(house.payment_history)
        self.assertTrue(house.proposed_jobs)
        self.assertFalse(house.pending_payments)

        #job
        job = Job.objects.get(pk=1)
        self.assertTrue(job.approved)
        self.assertFalse(job.rejected)
        self.assertEqual(job.pk, 1)
        self.assertEqual(job.house, house)
        self.assertEqual(job.company, self.worker)
        self.assertEqual(job.start_amount, 5000.00)
        self.assertEqual(job.balance_amount, 0.00)
        self.assertEqual(job.total_paid, 5000.00)
        self.assertEqual(job.document_link, '/worker_uploads/test2/pdf-sample.pdf')

        #payment
        payment = Request_Payment.objects.get(pk=1)
        self.assertTrue(payment.approved)
        self.assertFalse(payment.requested_by_worker)
        self.assertEqual(Request_Payment.objects.count(), 1)
        self.assertEqual(payment.amount, 5000.00)
        self.assertEqual(payment.job, job)

        #approve job POST
        response = self.c.post(
            '/jobs_admin/',
            {
                'job_id': 2,
                'approve_job': 'approve_job',
            }
        )

        #current worker
        self.assertEqual(Current_Worker.objects.count(), 1)

        #house
        house = House.objects.get(pk=1)
        self.assertTrue(house.completed_jobs)
        self.assertTrue(house.payment_history)
        self.assertTrue(house.proposed_jobs)
        self.assertFalse(house.pending_payments)

        #job
        job = Job.objects.get(pk=2)
        self.assertTrue(job.approved)
        self.assertFalse(job.rejected)
        self.assertEqual(job.pk, 2)
        self.assertEqual(job.house, house)
        self.assertEqual(job.company, self.worker)
        self.assertEqual(job.start_amount, 6080.00)
        self.assertEqual(job.balance_amount, 6080.00)
        self.assertEqual(job.total_paid, 0.00)
        self.assertEqual(job.document_link, '/worker_uploads/test2/pdf-sample.pdf-2')

        #reject job POST
        response = self.c.post(
            '/jobs_admin/',
            {
                'job_id': 3,
                'reject_estimate': 'reject_estimate',
            }
        )

        #current worker
        self.assertEqual(Current_Worker.objects.count(), 1)

        #house
        house = House.objects.get(pk=1)
        self.assertTrue(house.completed_jobs)
        self.assertTrue(house.payment_history)
        self.assertFalse(house.proposed_jobs)
        self.assertFalse(house.pending_payments)

        #job
        job = Job.objects.get(pk=3)
        self.assertFalse(job.approved)
        self.assertTrue(job.rejected)
        self.assertEqual(job.pk, 3)
        self.assertEqual(job.house, house)
        self.assertEqual(job.company, self.worker)
        self.assertEqual(job.start_amount, 7567.00)
        self.assertEqual(job.balance_amount, 7567.00)
        self.assertEqual(job.total_paid, 0.00)
        self.assertEqual(job.document_link, '/worker_uploads/test2/pdf-sample.pdf-3')
