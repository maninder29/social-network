from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
from friendship.models import Friend, Follow
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm


@login_required
def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
		"value":"Create",
	}
	return render(request, "post_form.html", context)

@login_required
def post_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	content_type=ContentType.objects.get_for_model(Post)
	object_id=instance.id
	comments=Comment.objects.filter(content_type=content_type, object_id=object_id, parent=None)
	form=CommentForm(request.POST or None)
	if form.is_valid():
		parent=None
		user=request.user
		content=form.cleaned_data.get("content")
		try:
			parent_id=int(request.POST.get("parent_id"))
		except:
			parent_id=None
		if parent_id:
			parent=get_object_or_404(Comment,id=parent_id)
		c=Comment(user=user,
			content_type=content_type,
			object_id=object_id,
			content=content,
			parent=parent)
		c.save()
		return redirect(instance)
	context = {
		"title": instance.title,
		"instance": instance,
		"img_list": ["jpg","JPG","jpeg","JPEG","png","PNG"],
		"vid_list": ["MP4","mp4","WebM","webm","WEBM"],
		"comments":comments,
		"form":form,
	}
	return render(request, "post_detail.html", context)

@login_required
def post_list(request):
	queryset_list = Post.objects.filter(
		Q(user=request.user)|
		Q(user__in=Friend.objects.friends(request.user))
		)
	paginator = Paginator(queryset_list, 2)
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list": queryset, 
		"img_list": ["jpg","JPG","jpeg","JPEG","png","PNG"],
		"vid_list": ["MP4","mp4","3GP","3gp","AVI","avi","MKV","mkv"],
	}
	return render(request, "base.html", context)

@login_required
def post_update(request, id=None):
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return redirect(instance)

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
		"value":"Save",
	}
	return render(request, "post_form.html", context)

@login_required
def post_delete(request,id):
	instance=get_object_or_404(Post, id=id)
	instance.delete()
	return redirect("posts:list")

