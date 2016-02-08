import hashlib

from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

from django.contrib.auth import get_user_model
User = get_user_model()

class ItemModelTest(TestCase):
	
	def test_cannot_save_empty_list_items(self):
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()

	def test_default_text(self):
		item = Item()
		self.assertEqual(item.text, '')

	def test_item_is_related_to_list(self):
		list_ = List.objects.create()
		item = Item()
		item.list = list_
		item.save()
		self.assertIn(item, list_.item_set.all())

	def test_duplicate_items_are_invalid(self):
		list_ = List.objects.create()
		item1 = Item.objects.create(list=list_, text='bla')
		with self.assertRaises(ValidationError):
			item2 = Item(list=list_, text='bla')
			item2.hash_text_field()
			item2.full_clean()

	
	def test_CAN_save_same_item_to_different_lists(self):
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='bla')
		item = Item(list=list2, text='bla')
		item.full_clean() # This should not raise an error

	def test_item_hashes_correctly(self):
		list_ = List.objects.create()
		item = Item.objects.create(text='hash me', list=list_)
		m = hashlib.md5('hash me'.encode('utf-8'))
		self.assertEqual(item.text_hash, m.hexdigest())

class ListModelTest(TestCase):

	def test_get_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))

	def test_create_new_creates_list_and_first_item(self):
		List.create_new(first_item_text='new item text')
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'new item text')
		new_list = List.objects.first()
		self.assertEqual(new_item.list, new_list)

	def test_create_new_optionally_saves_owner(self):
		user = User.objects.create()
		List.create_new(first_item_text='new item text', owner=user)
		new_list = List.objects.first()
		self.assertEqual(new_list.owner, user)

	def test_lists_can_have_owners(self):
		List(owner=User()) # should not raise

	def test_list_owner_is_optional(self):
		List().full_clean() # should not raise

	def test_create_new_returns_new_list_object(self):
		returned = List.create_new(first_item_text='new item text')
		new_list = List.objects.first()
		self.assertEqual(returned, new_list)

	def test_list_name_is_first_item_text(self):
		new_list = List.objects.create()
		Item.objects.create(text='first item text', list=new_list)
		Item.objects.create(text='second item text', list=new_list)
		self.assertEqual(new_list.name, 'first item text')
