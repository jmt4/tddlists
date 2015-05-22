from selenium import webdriver
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

		self.assertIn('To-Do', self.browser.title)	#5
		self.fail('Finish the test')	#6 -- this is simply a reminder to finish the test. self.fail automatically fails.
		#They notice the page title and header mention to-do list


		#They are allowed to create an item "to-do" immediately

		#They type in "Practice Django hard!"

		#Page updates when enter is hit

		#Another item can easily be added. It is

		#Page updates

		#They wonder if the items will be retained for future reference. In our app: Of course they will becaue they make an account
if __name__ == '__main__':	#7
	unittest.main(warnings='ignore')	#8