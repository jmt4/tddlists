from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		new_item_text = request.POST['item_text']
		Item.objects.create(text=new_item_text)#dont need to call save() if we use create
		return redirect('/lists/the-only-list-in-the-world/')
	return render(request, 'lists/home.html')

def view_list(request):
	items = Item.objects.all()
	return render(request, 'lists/list.html', {
		'items': items
	})
	#my_var = dict.get(<key>,<default>)
	#this is a way to get an item, and provide a default if that key does not exist
	#item.text = request.POST.get('item_text', '')

	#return render(request, 'lists/home.html', {
	#	'new_item_text': new_item_text,
	#})