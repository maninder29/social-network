from django import template

register = template.Library()

@register.filter
def has_liked(user, obj):
	return obj.liked_by_user(user)

