def friendship_add_friend(request, to_username, template_name='friendship/user_actions.html'):
    """ Create a FriendshipRequest """
    ctx = {'to_username': to_username,'error':False}
    if request.method == 'POST':
        to_user = user_model.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            ctx['error'] = True
        # else:
        #     return redirect('friendship_request_list')
    return render(request, template_name, ctx)