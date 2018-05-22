from django.test import TestCase
from django.test import Client
from jobs.models import House, Job, Request_Payment
from .views import send_data
from .send_data_extras import send_data_email
from django.core import mail
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
    def send_data_email_test(self, host, headers, queryset, attributes, user_email, title='TEST'):
        """Tests if the email in the 'send_data' view sends successfully"""

        form_vals={'send_to': 'andre.mashraghi@gmail.com', 'subject': 'Test Subject', 'message': 'This is a test.'}
        send_data_email(user_email=user_email, title=title, headers=headers, queryset=queryset, attributes=attributes, form_vals=form_vals, host=host)

        msg = mail.outbox[0]
        self.assertEqual(len(msg.attachments), 2)

        #test to see if attachments are on email
        self.assertEqual(msg.attachments[0][0], 'data.csv')
        self.assertEqual(msg.attachments[0][2], 'text/csv')
        self.assertEqual(msg.attachments[1][0], 'files.zip')
        self.assertEqual(msg.attachments[1][2], 'application/x-zip-compressed')

        self.assertEqual(msg.to, ['andre.mashraghi@gmail.com'])
        self.assertEqual(msg.subject, 'Test Subject')
        self.assertEqual(msg.body, 'This is a test.')
    def test_send_data_get(self):
        response = self.c.get('/send_data/')
        self.assertRedirects(response, '/payment_history/thank_you')
    def test_send_data_post(self):
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
            document_link='/worker_uploads/test2/pdf-sample.pdf',
            approved=True,
            rejected=False,
        )
        Request_Payment.objects.create(
            pk=1,
            house=house,
            job=job,
            amount=5000.00,
            requested_by_worker=False,
            approved=True,
        ).save()

        house.save()
        job.save()

        #test send_data_email function
        host = '127.000.001'

        jobs = Job.objects.filter(pk=1) #test for job querysets
        headers = ['House', 'Company', 'Start Amount', 'Balance', 'Submit Date', 'Total Paid']
        attributes = ['house', 'company', 'start_amount', 'balance', 'start_date', 'total_paid']
        self.send_data_email_test(user_email=self.customer.email, title='Test Send Data Jobs', headers=headers, queryset=jobs, attributes=attributes, host=host)

        payments = Request_Payment.objects.filter(pk=1) #test for payment querysets
        headers = ['House', 'Company', 'Amount', 'Submit Date', 'Contract Link']
        attributes = [['house', 'address'], ['job', 'company'], 'amount', 'submit_date', ['job', 'document_link']]
        self.send_data_email_test(user_email=self.customer.email, title='Test Send Data Payments', headers=headers, queryset=payments, attributes=attributes, host=host)

        #check if two emails were sent: one for jobs and one for payments
        self.assertEqual(len(mail.outbox), 2)

        response = self.c.post(
            '/send_data/',
            {
                'path': '/jobs_complete/',
                'send_to': 'andre.mashraghi@gmail.com',
                'subject': 'Test Subject',
                'message': 'Test message',
                'frequency': 1,
            }
        )

        #post
        self.assertEqual(response.status_code, 302)
        self.assertRaises(AttributeError) #job objects have no 'job' attribute

        #job
        job = Job.objects.get(pk=1)
        self.assertEqual(job.pk, 1)
        self.assertEqual(job.house, house)
        self.assertEqual(job.company, self.worker)
        self.assertEqual(job.start_amount, 5000.00)
        self.assertEqual(job.balance_amount, 0.00)
        self.assertEqual(job.total_paid, 5000.00)
        self.assertEqual(job.document_link, '/worker_uploads/test2/pdf-sample.pdf')
        self.assertTrue(job.approved)
        self.assertFalse(job.rejected)

        #payment
        payment = Request_Payment.objects.get(pk=1)
        self.assertEqual(payment.pk, 1)
        self.assertEqual(payment.house, house)
        self.assertEqual(payment.job, job)
        self.assertEqual(payment.job.company, self.worker)
        self.assertEqual(payment.amount, 5000.00)
        self.assertFalse(payment.requested_by_worker)
        self.assertTrue(payment.approved)

        self.assertRedirects(response, '/payment_history/thank_you')
