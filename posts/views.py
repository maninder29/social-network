from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from friendship.models import Friend, Follow
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from .forms import PostForm,CommentForm
from .models import Post,Comment,Like

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
		"instance": instance,
		"img_list": ["jpg","JPG","jpeg","JPEG","png","PNG","gif","GIF"],
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
		"img_list": ["jpg","JPG","jpeg","JPEG","png","PNG","gif","GIF"],
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

@login_required
def post_like(request, id):
	if request.is_ajax():
		post=Post.objects.get(id=id)
		user=request.user
		if post.liked_by_user(user):
			l=get_object_or_404(Like, user=user, post=post)
			l.delete()
			post.like_count-=1
			post.save()
			like_count=post.like_count
			data={"like_count":like_count, "like_status":'not liked'}
			return JsonResponse(data)
		l=Like(user=user, post=post)
		l.save()
		post.like_count+=1
		post.save()
		like_count=post.like_count
		data={"like_count":like_count, "like_status":'liked'}
		return JsonResponse(data)
	else:
		post=Post.objects.get(id=id)
		user=request.user
		if post.liked_by_user(user):
			l=get_object_or_404(Like, user=user, post=post)
			l.delete()
			post.like_count-=1
			post.save()
			return redirect("posts:list")
		l=Like(user=user, post=post)
		l.save()
		post.like_count+=1
		post.save()
		return redirect("posts:list")


def oh(request):
	return render(request, 'list.html', {})
# def user_detail(request,u):
# 	user=User.objects.get(username=u)
# 	friends=Friend.objects.friends(user)
# 	unread_friend_requests=Friend.objects.unread_requests(user=user)
# 	unrejected_friend_requests=Friend.objects.unrejected_requests(user=user)
# 	rejected_friend_requests=Friend.objects.rejected_requests(user=user)
# 	sent_friend_requests=Friend.objects.sent_requests(user=user)
# 	followers=Follow.objects.followers(user)
# 	following=Follow.objects.following(user)
# 	posts=Post.objects.filter(user=user)
# 	context={
# 		"current_user":user,
# 		"friends":friends,
# 		"unread_friend_requests":unread_friend_requests,
# 		"unrejected_friend_requests":unrejected_friend_requests,
# 		"rejected_friend_requests":rejected_friend_requests,
# 		"sent_friend_requests":sent_friend_requests,
# 		"followers":followers,
# 		"following":following,
# 		"posts":posts,
# 		"img_list": ["jpg","JPG","jpeg","JPEG","png","PNG","gif","GIF"],
# 		"vid_list": ["MP4","mp4","WebM","webm","WEBM"],
# 	}
# 	return render(request,"user_detail.html", context)