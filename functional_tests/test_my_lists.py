from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .server_tools import create_session_on_server

class MyListsTest(FunctionalTest):

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		# Edith is a logged-in user
		self.create_pre_authenticated_session('edith@example.com')

		# She goes to the home page and starts a list
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('Reticulate splines\n')
		self.get_item_input_box().send_keys('Immanetize eschaton\n')
		first_list_url = self.browser.current_url

		# She notices a "My lists" link for the first time
		self.browser.find_element_by_link_text('My lists').send_keys(Keys.RETURN)

		# She sees that her list is in there, named accoring to its
		# first list item
		link_element = self.wait_for_return_element(
			lambda: self.browser.find_element_by_link_text('Reticulate splines')
		)
		link_element.send_keys(Keys.RETURN)
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
		)

		# She decides to start another list, just to see
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('Click cows\n')
		second_list_url = self.browser.current_url

		# Under "My lists", her new list appears
		self.browser.find_element_by_link_text("My lists").send_keys(Keys.RETURN)
		link_element = self.wait_for_return_element(
			lambda: self.browser.find_element_by_link_text('Click cows')
		)
		link_element.send_keys(Keys.RETURN)
		self.assertEqual(self.browser.current_url, second_list_url)

		# She logs out. The "My lists" option disappears
		self.browser.find_element_by_id('id_logout').send_keys(Keys.RETURN)
		self.assertEqual(
			self.browser.find_elements_by_link_text('My lists'),
			[]
		)