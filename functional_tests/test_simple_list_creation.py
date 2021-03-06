from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

	def test_can_start_a_list_and_retrieve_it_later(self):	#4

		#Some user wants to check out the homepage of a to-do list web application.
		self.browser.get(self.server_url)

		#They visit the site. 

		self.assertIn('To-Do', self.browser.title) #5
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#They are allowed to create an item "to-do" immediately
		inputbox = self.get_item_input_box()
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#They type in "Practice Django hard!" into the textbox, then hit enter.
		inputbox.send_keys('Practice Django hard!')
		inputbox.send_keys(Keys.ENTER)
		jim_list_url = self.browser.current_url
		self.assertRegex(jim_list_url, '/lists/.+', msg=jim_list_url)
		self.check_for_row_in_list_table('1: Practice Django hard!')

		#Another item can easily be added. It is
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Practice Django harder!')
		inputbox.send_keys(Keys.ENTER)
	
		self.check_for_row_in_list_table('2: Practice Django harder!')
		self.check_for_row_in_list_table('1: Practice Django hard!')

		#A new user Francis visits the site

		## We use a new browser session to make sure that no information
		## of Jim's is coming through from the cookies etc.
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis vists the home page. There is no sign of Edith's
		# list
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Practice Django hard!', page_text)
		self.assertNotIn('Practice Django harder!', page_text)

		# Francis starts a new list by entering a new item. He
		# is less interesting than Jim ...
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		# Francis gets his own URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, jim_list_url)

		# Again, there is no trace of Jim's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Practice Django hard!', page_text)
		self.assertNotIn('Practice Django harder!', page_text)
		self.assertIn('Buy milk', page_text)

		#Satisfied, they both go back to sleep

		#self.fail('Finish the test!')	#6 -- this is simply a reminder to finish the test. self.fail automatically fails.