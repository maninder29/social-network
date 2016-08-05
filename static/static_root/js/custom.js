var dialog = document.querySelector('dialog');
if (! dialog.showModal) {
  dialogPolyfill.registerDialog(dialog);
}

$(".reply-btn").click(function(event){
  event.preventDefault();
  $(this).parent().parent().parent().parent().next(".comment-reply").fadeToggle();
})

$(".like-btn").click(function(event){
  event.preventDefault();
  var self = $(this);
  var button = self.children('button');
  var span = self.siblings('span.like-count');
  var n = parseInt(span.text());
  var string = button.attr('class');
  var sub = 'mdl-button--accent';
  if (string.indexOf(sub) != -1) {
    span.text(n-1);
  }else{
    span.text(n+1)
  }
  button.toggleClass(sub)
  $.ajax({
    url:self.attr("href"),
    type:'get',
    failure: function(response, error){
      console.log(error);
      window.location=self.attr("href")
    }
  })
})

$(".add-friend-btn").click(function(event){
  event.preventDefault();
  ctx={}
  $.ajax({
    url:$(".add-friend-btn").parent().attr("action"),
    type:'get',
    data:ctx,
    success: function(data){
      if (data.error) {
        var notification = document.querySelector('.mdl-js-snackbar');
        notification.MaterialSnackbar.showSnackbar({
          message: 'You are already friend of '+ data.to_username, timeout: 5000
        });
      } else{
        var notification = document.querySelector('.mdl-js-snackbar');
        notification.MaterialSnackbar.showSnackbar({
          message: 'Friend request sent successfully :)', timeout: 5000
        });
      }
    },
    failure: function(error){
      console.log(error)
      $(".add-friend-btn").click()
    }
  })
})

$(".follow-btn").click(function(event){
  event.preventDefault();
  ctx={}
  $.ajax({
    url:$(".follow-btn").parent().attr("action"),
    type:'get',
    data:ctx,
    success: function(data){
      if (data.error) {
        var notification = document.querySelector('.mdl-js-snackbar');
        notification.MaterialSnackbar.showSnackbar({
          message: 'You have already started following '+ data.followee_username
        });
      } else if (data.are_friends) {
        var notification = document.querySelector('.mdl-js-snackbar');
        notification.MaterialSnackbar.showSnackbar({
          message: 'You both are already friends'
        });
      } else {
        var notification = document.querySelector('.mdl-js-snackbar');
        notification.MaterialSnackbar.showSnackbar({
          message: 'You have successfully started following '+ data.followee_username
        });
      }
    },
    failure: function(error){
      console.log(error)
      $(".follow-btn").click()
    }
  })
})

$(".post-delete-btn").click(function(event){
  event.preventDefault();
  var dialog = document.querySelector('dialog.mdl-dialog-post-delete');
  dialog.showModal();
  dialog.querySelector('.agree').addEventListener('click', function() {
    window.location=$(".post-delete-btn").attr("href")
  });
  dialog.querySelector('.close').addEventListener('click', function() {
    dialog.close();
  });
})