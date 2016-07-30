from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_delete, post_save
from django.db import models
import os



def media_upload(instance, filename):
    return '{0}/{1}'.format(instance.user.username, filename)


class Post(models.Model):
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    media = models.FileField(upload_to=media_upload, null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    def extension(self):
        name, extension = os.path.splitext(self.media.name)
        return extension[1:]

    def liked_by_user(self, user):
        if Like.objects.filter(post=self, user=user).exists():
            return True
        return False

    class Meta:
        ordering = ["-timestamp","-updated"]


class Like(models.Model):
    user=models.ForeignKey(User)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    def __unicode__(self):
        return str(self.user)


class Comment(models.Model):
    user=models.ForeignKey(User)
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

def profile_pic_upload(instance, filename):
    return'{0}/{1}/{2}'.format(instance.user.username, 'profile_pictures', filename)

GENDER_CHOICES=(
    ('male,Male'),
    ('female','Female'),
    ('other','Other')
)

RELATIONSHIP_CHOICES=(
    ('single','Single'),
    ('married','Married'),
    ('complicated',"It's complicated" )
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_pic = models.ImageField(upload_to=profile_pic_upload, default='default.png', null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)#, choices=GENDER_CHOICES)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    relationship_status = models.CharField(max_length=20, null=True, blank=True)#, choices=RELATIONSHIP_CHOICES)
    def __unicode__(self):
        return self.user.username


def user_profile_post_save_reciever(instance, created, *args, **kwargs):
    if created:
        u=UserProfile(user=instance)
        u.save()

def post_pre_delete_reciever(sender,instance,*args,**kwargs):
    content_type=ContentType.objects.get_for_model(sender)
    object_id=instance.id
    comments=Comment.objects.filter(content_type=content_type, object_id=object_id)
    for c in comments:
        for r in c.children():
            r.delete()
        c.delete()
    path=settings.MEDIA_PATH+"\\"+str(instance.media)
    try:
        os.remove(path)
    except:
        pass


post_save.connect(user_profile_post_save_reciever, sender=User)

pre_delete.connect(post_pre_delete_reciever, sender=Post)
