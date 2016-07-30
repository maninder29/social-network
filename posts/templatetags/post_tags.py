from django import template
from posts.models import Like

register = template.Library()

@register.filter
def has_liked(user, obj):
	return obj.liked_by_user(user)

@register.inclusion_tag('likers.html')
def liked_by_users(obj):
	return {'likers' : Like.objects.filter(post=obj)}