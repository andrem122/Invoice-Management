from django.test import TestCase
from django.test import Client
from .views import approved_payments

class Test_Payment_Requests(TestCase):
    def setUp(self):
        self.c = Client()
    def test_approved_payments(self):
        response = self.c.post(
            'payment_requests/approved_payments',
            {'p_id': 30, 'job_id': 3, 'job_house': '1234 Old Fart Way'}
        )
