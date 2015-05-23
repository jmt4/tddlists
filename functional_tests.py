from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):	#1

	def setUp(self):	#2
		self.browser = webdriver.Firefox() #we start the browser here
		self.browser.implicitly_wait(3) #this makes sure we wait after the browser has been started and ensures the page has loaded

	def tearDown(self):	#3
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):	#4

		#Some user wants to check out the homepage of a to-do list web application.
		#They visit the site. 
		self.browser.get('http://localhost:8000')

		self.assertIn('To-Do', self.browser.title) #5
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#They are allowed to create an item "to-do" immediately
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#They type in "Practice Django hard!"
		inputbox.send_keys('Practice Django hard!')

		#Page updates when enter is hit
		inputbox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Practice Django hard!' for row in rows)
		)

		#Another item can easily be added. It is
		self.fail('Finish the test')	#6 -- this is simply a reminder to finish the test. self.fail automatically fails.
		#They notice the page title and header mention to-do list

		#Page updates

		#They wonder if the items will be retained for future reference. In our app: Of course they will becaue they make an account
if __name__ == '__main__':	#7
	unittest.main(warnings='ignore')	#8