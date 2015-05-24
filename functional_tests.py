from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	#the setUp() method is overridden from TestCase. It does nothing by itself
	def setUp(self):
		self.browser = webdriver.Firefox() #we start the browser here
		self.browser.implicitly_wait(3) #this makes sure we wait after the browser has been started and ensures the page has loaded

	#Similarly, tearDown is inherited from TestCase and overriden with our own functionality here
	def tearDown(self):
		self.browser.quit()
	"""
	Helper methods -- unless method starts with test_ it isn't run as a test.
	Thus we can use it to 'help' make the test better.
	"""

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])


	"""
	---Functional Tests---
	"""

	def test_can_start_a_list_and_retrieve_it_later(self):	#4

		#Some user wants to check out the homepage of a to-do list web application.
		self.browser.get('http://localhost:8000')

		#They visit the site. 
		self.assertIn('To-Do', self.browser.title) #5
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#They are allowed to create an item "to-do" immediately
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#They type in "Practice Django hard!" into the textbox, then hit enter.
		inputbox.send_keys('Practice Django hard!')
		inputbox.send_keys(Keys.ENTER)
		self.check_for_row_in_list_table('1: Practice Django hard!')

		#Another item can easily be added. It is
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Practice Django harder!')
		inputbox.send_keys(Keys.ENTER)
		self.check_for_row_in_list_table('1: Practice Django hard!')
		self.check_for_row_in_list_table('2: Practice Django harder!')

		self.fail('Finish the test')	#6 -- this is simply a reminder to finish the test. self.fail automatically fails.
		#They notice the page title and header mention to-do list

		#Page updates

		#They wonder if the items will be retained for future reference. In our app: Of course they will becaue they make an account
if __name__ == '__main__':	#7
	unittest.main(warnings='ignore')	#8