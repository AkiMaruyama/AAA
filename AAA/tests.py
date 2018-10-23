from django.test import TestCase
from .views import *
# Create your tests here.

class ViewTestCase(TestCase):
    def setUp(self):
        pass
    def test_get_paras(self):
        """"""
        self.assertEqual(len(get_paras(1)), 2)
        self.assertEqual(len(get_paras(2)), 2)
        self.assertEqual(len(get_paras(3)), 2)
        # self.assertEqual(cat.speak(), 'The cat says "meow"')
