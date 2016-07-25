from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
user_model = User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

#from django.utils.safestring import mark_safe
from friendship.exceptions import AlreadyExistsError
from friendship.models import Friend, Follow, FriendshipRequest

get_friendship_context_object_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user')
get_friendship_context_object_list_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users')


def view_friends(request, username, template_name='friendship/friend/user_list.html'):
    """ View the friends of a user """
    user = get_object_or_404(user_model, username=username)
    friends = Friend.objects.friends(user)
    # return render(request, template_name, {get_friendship_context_object_name(): user, 'friends': friends})
    return render(request, template_name, {'c_user': user, 'friends': friends})


@login_required
def friendship_add_friend(request, to_username, template_name='user_detail.html'):
    """ Create a FriendshipRequest """
    ctx = {'to_username': to_username,'error':False}
    if request.method == 'GET' and request.is_ajax():
        to_user = user_model.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except Exception as e:
            print e
            ctx['error'] = True
        return JsonResponse(ctx)
    return redirect("/")


@login_required
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.accept()
        return redirect(reverse('user_detail', kwargs={'u':request.user.username}))
    return redirect('/')


@login_required
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.reject()
        return redirect(reverse('user_detail', kwargs={'u':request.user.username}))
    return redirect('/')


@login_required
def friendship_cancel(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_sent,
            id=friendship_request_id)
        f_request.cancel()
        return redirect(reverse('user_detail', kwargs={'u':request.user.username}))
    return redirect('/')


@login_required
def friendship_remove(request, username):
    """ remove a friend """
    if request.method == 'POST':
        friend = user_model.objects.get(username=username)
        user=request.user
        Friend.objects.remove_friend(friend, user)
        return redirect(reverse('user_detail', kwargs={'u':request.user.username}))
    return redirect('/')


@login_required
def friendship_request_list(request, template_name='friendship/friend/requests_list.html'):
    """ View unread and read friendship requests """
    # friendship_requests = Friend.objects.requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {'requests': friendship_requests})


@login_required
def friendship_request_list_rejected(request, template_name='friendship/friend/requests_list.html'):
    """ View rejected friendship requests """
    # friendship_requests = Friend.objects.rejected_requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {'requests': friendship_requests})


def followers(request, username, template_name='friendship/follow/followers_list.html'):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    followers = Follow.objects.followers(user)

    return render(request, template_name, {get_friendship_context_object_name(): user, 'followers': followers})


def following(request, username, template_name='friendship/follow/following_list.html'):
    """ List who this user follows """
    user = get_object_or_404(user_model, username=username)
    following = Follow.objects.following(user)

    return render(request, template_name, {get_friendship_context_object_name(): user, 'following': following})


@login_required
def follower_add(request, followee_username, template_name='user_detail.html'):
    """ Create a following relationship """
    ctx = {'followee_username': followee_username, 'error':False, 'are_friends':False}
    if request.method == 'GET' and request.is_ajax():
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        if Friend.objects.are_friends(followee, follower):
            ctx['are_friends'] = True
        else:
            try:
                Follow.objects.add_follower(follower, followee)
            except Exception as e:
                print e
                ctx['error'] = True
        return JsonResponse(ctx)
    else:
        return redirect("/")


@login_required
def followee_remove(request, followee_username, template_name='friendship/follow/remove.html'):
    """ Remove a following relationship by the follwer"""
    if request.method == 'POST':
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        Follow.objects.remove_follower(follower, followee)
        return redirect(reverse('user_detail', kwargs={'u':request.user.username}))
    return render('/')

@login_required
def follower_remove(request, follower_username, template_name='friendship/follow/remove.html'):
    """ Remove a following relationship by the one whos being followed """
    if request.method == 'POST':
        followee = request.user
        follower = user_model.objects.get(username=follower_username)
        Follow.objects.remove_follower(follower, followee)
        return redirect(reverse('user_detail', kwargs={'u':request.user.username}))
    return render('/')


def all_users(request, template_name="friendship/user_actions.html"):
    ctx={}
    query=request.GET.get("q")
    if query:
        users=user_model.objects.filter(
            (Q(username__icontains=query)|
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query))&
            ~Q(id=request.user.id)&
            Q(is_active=True)
            )
    else:
        users = user_model.objects.exclude(id=request.user.id).filter(is_active=True)
    ctx[get_friendship_context_object_list_name()]=users
    if len(users)>0:
        return render(request, template_name, ctx)
    else:
        return HttpResponse("<h2>No matches found :(")
