from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.template import Context
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from django.contrib.auth import get_user_model

import unittest
from unittest import skip
from unittest.mock import Mock, patch

from lists.views import home_page, new_list, new_list2
from lists.models import Item, List
from lists.forms import (
	EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, 
	ItemForm, ExistingListItemForm,
)

User = get_user_model()

class NewListTest(TestCase):

	def test_invalid_test_items_arent_saved(self):
		self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)

	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'lists/home.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_home_page_can_save_POST_request(self):
		self.client.post(
			'/lists/new',
			data = {
				'text': 'A new list item',
			}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_home_page_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data = {
				'text': 'A new item list',
			}
		)
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id))

class HomePageTest(TestCase):
	maxDiff = None

	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'lists/home.html')

	def test_home_page_uses_item_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], ItemForm)

class ListViewTest(TestCase):

	"""
	Helper Methods
	"""
	def post_invalid_input(self):
		list_ = List.objects.create()
		return self.client.post(
			'/lists/%d/' % (list_.id,),
			data = {'text': ''}
		)

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id))
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other item 1', list=other_list)
		Item.objects.create(text='other item 2', list=other_list)

		response = self.client.get('/lists/%d/' % (correct_list.id))

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other item 1')
		self.assertNotContains(response, 'other item 2')

	def test_list_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id))
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/lists/%d/' % (correct_list.id,),
			data = {
				'text': 'A new item for existing list'
			}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_POST_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/' % (correct_list.id,),
			data = {
				'text': 'A new item for existing list'
			})

		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

	def test_displays_item_form(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertIsInstance(response.context['form'], ExistingListItemForm)
		self.assertContains(response, 'name="text"')

	def test_for_invalid_input_nothing_saved_to_db(self):
		self.post_invalid_input()
		self.assertEqual(Item.objects.count(), 0)

	def test_for_invalid_input_renders_list_template(self):
		response = self.post_invalid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'], ExistingListItemForm)

	def test_for_invalid_input_shows_error_on_page(self):
		response = self.post_invalid_input()
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))
	
	def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
		list1 = List.objects.create()
		Item.objects.create(list=list1, text='textey')
		response = self.client.post(
			'/lists/%d/' % (list1.id,),
			data={'text': 'textey'} 
		)

		expected_error = escape("You've already got this in your list")

		self.assertContains(response, expected_error)
		self.assertTemplateUsed(response, 'lists/list.html')
		self.assertEqual(Item.objects.all().count(), 1)

class MyListsIntegratedTest(TestCase):

	def test_list_owner_is_saved_if_user_is_authenticated(self):
		request = HttpRequest()
		request.user = User.objects.create(email='a@b.com')
		request.POST['text'] = 'new list item'
		new_list(request)
		list_ = List.objects.first()
		self.assertEqual(list_.owner, request.user)

@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

	def setUp(self):
		self.request = HttpRequest()
		self.request.POST['text'] = 'this is text'
		self.request.user = User()

		self.message = "Method should not be called. Called {times} times!"

	def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
		new_list(self.request)
		mockNewListForm.assert_called_once_with(data=self.request.POST)

	def test_saves_form_with_owner_if_form_is_valid(self, mockNewListForm):
		mock_form = mockNewListForm.return_value
		mock_form.is_valid.return_value = True
		new_list(self.request)
		mock_form.save.assert_called_once_with(owner=self.request.user)

	def test_save_not_called_if_form_is_invalid(self, mockNewListForm):
		mock_form = mockNewListForm.return_value
		mock_form.is_valid.return_value = False
		new_list(self.request)
		self.assertFalse(mock_form.save.called,
						 self.message.format(times=mockNewListForm.call_count))

	@patch('lists.views.redirect')
	def test_redirects_to_form_returned_object_if_form_valid(
		self, mock_redirect, mockNewListForm
	):
		mock_form = mockNewListForm.return_value
		mock_form.is_valid.return_value = True

		response = new_list(self.request)

		self.assertEqual(response, mock_redirect.return_value)
		mock_redirect.assert_called_once_with(mock_form.save.return_value)

	@patch('lists.views.render')
	def test_renders_home_template_with_form_if_form_invalid(
		self, mock_render, mockNewListForm
	):
		mock_form = mockNewListForm.return_value
		mock_form.is_valid.return_value = False
		
		response = new_list(self.request)
		
		self.assertEqual(response, mock_render.return_value)
		mock_render.assert_called_once_with(
			self.request, 'lists/home.html', {'form': mock_form}
		)