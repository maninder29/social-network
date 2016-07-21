from django.contrib.auth.models import User
from friendship.models import Friend, Follow
from django.shortcuts import render,redirect

def home(request):
	return redirect("posts:list")

def user_detail(request,u):
	user=User.objects.get(username=u)
	friends=Friend.objects.friends(user)
	unread_friend_requests=Friend.objects.unread_requests(user=user)
	unrejected_friend_requests=Friend.objects.unrejected_requests(user=user)
	rejected_friend_requests=Friend.objects.rejected_requests(user=user)
	sent_friend_requests=Friend.objects.sent_requests(user=user)
	followers=Follow.objects.followers(user)
	following=Follow.objects.following(user)
	context={
		"user":user,
		"friends":friends,
		"unread_friend_requests":unread_friend_requests,
		"unrejected_friend_requests":unrejected_friend_requests,
		"rejected_friend_requests":rejected_friend_requests,
		"sent_friend_requests":sent_friend_requests,
		"followers":followers,
		"following":following
	}
	return render(request,"user_detail.html", context)
