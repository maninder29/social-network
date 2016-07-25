from django.contrib.auth.models import User
from friendship.models import Friend, Follow
from django.shortcuts import render,redirect
from posts.models import Post


def user_detail(request,u):
	user=User.objects.get(username=u)
	friends=Friend.objects.friends(user)
	followers=Follow.objects.followers(user)
	following=Follow.objects.following(user)
	unread_friend_requests=Friend.objects.unread_requests(user=user)
	unrejected_friend_requests=Friend.objects.unrejected_requests(user=user)
	rejected_friend_requests=Friend.objects.rejected_requests(user=user)
	sent_friend_requests=Friend.objects.sent_requests(user=user)
	posts=Post.objects.filter(user=user)
	context={
		"current_user":user,
		"friends":friends[:6],
		"followers":followers[:6],
		"following":following[:6],
		"unread_friend_requests":unread_friend_requests,
		"unrejected_friend_requests":unrejected_friend_requests,
		"rejected_friend_requests":rejected_friend_requests,
		"sent_friend_requests":sent_friend_requests,
		"posts":posts,
		"img_list": ["jpg","JPG","jpeg","JPEG","png","PNG","gif","GIF"],
		"vid_list": ["MP4","mp4","WebM","webm","WEBM"],
	}
	return render(request,"user_detail.html", context)
