from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item

class NewListTest(TestCase):

	def test_home_page_can_save_POST_request(self):
		self.client.post(
			'/lists/new',
			data = {
				'item_text': 'A new list item',
			}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_home_page_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data = {
				'item_text': 'A new item list',
			}
		)
		#self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('lists/home.html')
		self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		"""
		Below we are creating two Items, setting the text field in the model to some string,
		and, finally, saving them.
		"""
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'The second item'
		second_item.save()

		#returns QuerySet
		saved_items = Item.objects.all()
		"""
		The count method hits the database and returns the number of records.
		This is preferable if the QuerySet isn't cached (i.e stored in a variable)
		because we dont need to iterate over all the objects anyways.
		"""
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		"""
		Need to grab text with .text because we assign the objects, not their variables
		above.
		"""
		self.assertEqual(first_saved_item.text, first_item.text)
		self.assertEqual(second_saved_item.text, second_item.text)

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_displays_all_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')