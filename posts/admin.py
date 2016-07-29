from django.contrib import admin

# Register your models here.
from .models import Post,Comment,Like,UserProfile

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["user", "updated", "timestamp", "like_count"]
	list_display_links = ["updated"]
	list_filter = ["updated", "timestamp"]
	search_fields = ["content"]
	class Meta:
		model = Post


admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(UserProfile)
