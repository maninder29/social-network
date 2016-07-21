from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Comment(models.Model):
	user=models.ForeignKey(User)
	#post=models.ForiegnKey(Post)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	content=models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True, auto_now=False)
	parent=models.ForeignKey("self", null=True, blank=True)

	class Meta:
		ordering=["-timestamp"]

	def __unicode__(self):
		return str(self.user.username)+" - "+self.content[:10]

	def children(self):
		return Comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is None:
			return True
		return False