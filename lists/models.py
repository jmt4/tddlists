from django.db import models

# Create your models here.
"""
class Item: <-- this declaration 'implicitly' inherits from emph(object)
class Item(object): <-- this declaration 'explicitly' inherits from emph(object)
"""
class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)