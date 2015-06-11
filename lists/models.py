from django.db import models
from django.core.urlresolvers import reverse
import hashlib

# Create your models here.
"""
class Item: <-- this declaration 'implicitly' inherits from emph(object)
class Item(object): <-- this declaration 'explicitly' inherits from emph(object)
"""
class List(models.Model):
	
	def get_absolute_url(self):
		return reverse('view_list', args=[self.id])

class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)
	text_hash = models.CharField(default='', max_length=256, blank=True)

	class Meta:
		ordering = ('id',)
		unique_together = ('list', 'text_hash')

	def save(self, *args, **kwargs):
		self.hash_text_field()
		super(Item, self).save(*args, **kwargs)

	def __str__(self):
		return self.text

	def hash_text_field(self):
		hash = hashlib.md5(self.text.encode('utf-8')).hexdigest()
		self.text_hash = hash if len(hash) < 257 else hash[:256]
		#return hash if len(hash) < 257 else hash[:256]