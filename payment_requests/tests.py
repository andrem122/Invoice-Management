from django.test import TestCase
from django.test import Client
from .views import approved_payments
from django.contrib.auth.models import User, Group
from jobs.models import Job, House, Request_Payment

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
        response = self.c.get('/payments')
        self.assertEqual(response.status_code, 200)
    def test_approved_payments_by_worker(self):
        """
        Test if values for house, job, payment
        are correct after unapproving a payment for a house that originally
        had 1 completed job, had 1 approved payment, had 0
        pending payments, had 0 proposed_jobs, and payment with
        attribute created_by_system=True
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
            rejected=False,
        )
        payment = Request_Payment.objects.create(
            pk=1,
            house=house,
            job=job,
            amount=4000.00,
            created_by_system=True,
            approved=True,
        )

        house.save()
        job.save()
        payment.save()

        response = self.c.post('/payments', {'job_id': '1', 'p_id': '1'})
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
        self.assertFalse(job.rejected)

        payment = Request_Payment.objects.get(pk=1)
        self.assertFalse(payment.approved)
        self.assertTrue(payment.created_by_system)
        self.assertEqual(float(payment.amount), 4000.00)
        self.assertEqual(payment.job, job)
        self.assertEqual(payment.house, house)

        #check redirection after POST request is successful
        self.assertRedirects(response, '/payments')

    def test_approved_payments_by_code(self):
        """
        Test if values for house, job, payment
        are correct after unapproving a payment for a house that originally
        had 1 completed job, had 1 approved payment, had 0
        pending payments, had 0 proposed_jobs, and payment with
        attribute created_by_system=False
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
            rejected=False,
        )
        payment = Request_Payment.objects.create(
            pk=1,
            house=house,
            job=job,
            amount=7354.43,
            created_by_system=False,
            approved=True,
        )

        house.save()
        job.save()
        payment.save()

        response = self.c.post('/payments', {'job_id': '1', 'p_id': '1'})
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
        self.assertFalse(job.rejected)

        payment = Request_Payment.objects.filter(pk=1).exists()
        self.assertFalse(payment)

        #check redirection after POST request is successful
        self.assertRedirects(response, '/payments')
    def test_approved_payments_multiple_payments(self):
        """
        Test if values for house, job, payment
        are correct after unapproving a payment for a house that originally
        had 1 completed jobs, had 2 approved payments, had 2
        pending payments, had 0 proposed_jobs, and payment with
        attribute created_by_system=False
        """
        #create test data
        house = House.objects.create(
            pk=1,
            address='1234 N Test Way',
            customer=self.customer,
            completed_jobs=True,
            payment_history=True,
            proposed_jobs=False,
            pending_payments=True,
        )
        #job that is completed with 2 approved payments
        job = Job.objects.create(
            pk=1,
            house=house,
            company=self.worker,
            start_amount=5254.78,
            balance_amount=0.00,
            total_paid=5254.78,
            document_link='worker_uploads/house/file.ext',
            approved=True,
            rejected=False,
        )
        #2nd completed job
        Job.objects.create(
            pk=2,
            house=house,
            company=self.worker,
            start_amount=5700.78,
            balance_amount=0.00,
            total_paid=5700.78,
            document_link='worker_uploads/house_1/file.ext',
            approved=True,
            rejected=False,
        ).save()
        #2 approved payments for the first completed job
        Request_Payment.objects.create(
            pk=1,
            house=house,
            job=job,
            amount=3006.24,
            created_by_system=True,
            approved=True,
        ).save()
        Request_Payment.objects.create(
            pk=2,
            house=house,
            job=job,
            amount=2248.54,
            created_by_system=True,
            approved=True,
        ).save()

        house.save()
        job.save()

        response = self.c.post('/payments', {'job_id': '1', 'p_id': '2'})
        #check if values are correct after POST request
        house = House.objects.get(pk=1)
        self.assertTrue(house.pending_payments)
        self.assertTrue(house.completed_jobs)
        self.assertTrue(house.payment_history)
        self.assertFalse(house.proposed_jobs)

        #the job with the 2 approved payments
        active_job = Job.objects.get(pk=1)
        self.assertEqual(float(active_job.balance_amount), 2248.54)
        self.assertEqual(float(active_job.start_amount), 5254.78)
        self.assertEqual(float(active_job.total_paid), 3006.24)
        self.assertTrue(active_job.approved)
        self.assertEqual(active_job.house, house)
        self.assertEqual(active_job.document_link, 'worker_uploads/house/file.ext')
        self.assertEqual(active_job.company, self.worker)
        self.assertFalse(active_job.rejected)

        payment_approved_1 = Request_Payment.objects.get(pk=1)
        self.assertEqual(payment_approved_1.house, house)
        self.assertEqual(payment_approved_1.job, active_job)
        self.assertEqual(float(payment_approved_1.amount), 3006.24)
        self.assertTrue(payment_approved_1.created_by_system)
        self.assertTrue(payment_approved_1.approved)

        payment_approved_2 = Request_Payment.objects.get(pk=2)
        self.assertEqual(payment_approved_2.house, house)
        self.assertEqual(payment_approved_2.job, active_job)
        self.assertEqual(float(payment_approved_2.amount), 2248.54)
        self.assertTrue(payment_approved_2.created_by_system)
        self.assertFalse(payment_approved_2.approved)

        #check redirection after POST request is successful
        self.assertRedirects(response, '/payments')
