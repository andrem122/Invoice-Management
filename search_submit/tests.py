from django.test import TestCase
from .views import Search_Submit_View
from django.test import Client

class Test_Search(TestCase):
    def setUp(self):
        self.c = Client()
    def test_values_normalize_query(self):
        #test to see if incorrect data types are dealt with
        search_submit_view = Search_Submit_View()
        self.assertRaises(ValueError, search_submit_view.normalize_query, True)
        self.assertRaises(ValueError, search_submit_view.normalize_query, 2)
        self.assertRaises(ValueError, search_submit_view.normalize_query, ['list', 'list'])
        self.assertRaises(ValueError, search_submit_view.normalize_query, {'key': 1, 'key': '1'})
    def test_post(self):
        response = self.c.post('/search/', {'search': 'all'})
        self.assertEqual(response.status_code, 302)
        response = self.c.post('/search/', {'search': 'test'})
        self.assertEqual(response.status_code, 302)
    def test_get(self):
        response = self.c.get('/search/')
        self.assertEqual(response.status_code, 302)
