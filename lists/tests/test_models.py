from django.test import TestCase
from lists.models import Item, List

class ListAndItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		"""
		Below we are creating two Items, setting the text field in the model to some string,
		and, finally, saving them.
		"""
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'The second item'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

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
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, second_item.text)
		self.assertEqual(second_saved_item.list, list_)