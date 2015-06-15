from .base import FunctionalTest

from unittest import skip
from selenium.webdriver.common.action_chains import ActionChains

class ItemValidationTest(FunctionalTest):

	"""
	Helper Methods
	"""

	def get_error_element(self):
		return self.browser.find_element_by_css_selector('.has-error')

	"""
	Functional test_cannot_add_duplicate_items
	"""
	
	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('\n')

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		error = self.get_error_element()
		self.assertEqual(error.text, "You can't have an empty list item")

		# She tries again with some text for the item, which now works
		self.get_item_input_box().send_keys('Buy milk\n')
		self.check_for_row_in_list_table('1: Buy milk')

		# Perversely, she now decides to submit a second blank list item
		self.get_item_input_box().send_keys('\n')

		# She recieves a similar warning on the list page
		error = self.get_error_element()
		self.assertEqual(error.text, "You can't have an empty list item")

		# And she can correct it by filling some text inputbox
		self.get_item_input_box().send_keys('Make tea\n')
		self.check_for_row_in_list_table('1: Buy milk')
		self.check_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):
		# Edith goes to the home page and starts a new list
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('Buy wellies\n')
		self.check_for_row_in_list_table('1: Buy wellies')

		# She accidentally tries to enter a duplicate item
		self.get_item_input_box().send_keys('Buy wellies\n')

		# She sees a helpful error message
		self.check_for_row_in_list_table('1: Buy wellies')
		error = self.get_error_element()
		self.assertEqual(error.text, "You've already got this in your list")

	def test_error_messages_are_cleared_on_input(self):
		# Edith starts a new list in a way that causes a validation error:
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('\n')
		error = self.get_error_element()
		self.assertTrue(error.is_displayed())

		# She starts typing in the input box to clear the error
		self.get_item_input_box().send_keys('a')

		# She is pleased to see that the error message disappears
		error = self.get_error_element()
		self.assertFalse(error.is_displayed())

	def test_error_messages_are_cleared_when_input_box_is_clicked_on(self):
		# Edith starts a new list in a way that causes a validation error:
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('\n')
		error = self.get_error_element()
		self.assertTrue(error.is_displayed())

		# She clicks on the input box to clear the error message
		import time
		inputbox = self.get_item_input_box()
		actions = ActionChains(self.browser)
		actions.move_to_element(inputbox).perform()
		time.sleep(1)
		actions.click(inputbox).perform()
		time.sleep(1)
		#actions.perform()

		# She is pleased to see that the error message disappears
		error = self.get_error_element()
		self.assertFalse(error.is_displayed())