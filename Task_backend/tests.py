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
        
    def test_status_change(self, ):
        self.selenium.get('%s%s' % (self.live_server_url, '/tasks/main/'))
        task_row_list = self.selenium.find_elements_by_class('task_row')
        
        for row in task_row_list:
            mark_done = row.selenium.find_element_by_class('mark_done')
            mark_done.selenium.find_element_by_class('done').click()
            mark_dismissed = row.selenium.find_element_by_class('mark_dismissed')
            mark_dismissed.selenium.find_element_by_class('dismissed').click()
            delete = row.selenium.find_element_by_class('delete')
            delete.selenium.find_element_by_class('delete').click()
