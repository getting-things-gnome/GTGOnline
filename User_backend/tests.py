"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class MySeleniumTests(LiveServerTestCase):
    fixtures = ['user-data.json']
    
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()
        
    def test_login(self, ):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/landing/'))
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('cole')
        password_input = self.selenium.find_element_by_id('password')
        password_input.send_keys('cole')
        self.selenium.find_element_by_id('log_in').click()
