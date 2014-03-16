function reply_callback(json){
  if (json['success']){
      location.reload();
  } else {
      window.reply_lock = false;
    if (json['error'] == 1){
      $('#reply_nocontent_alert').hide();
      $('#reply_notlogin_alert').show();
    }
    if(json['error'] == 2){
      $('#reply_notlogin_alert').hide();
      $('#reply_nocontent_alert').show();
    }
  }
}

function reply_thread() {
    if (window.reply_lock) return;
    window.reply_lock = true;
    content =  $('#reply_form textarea').val();
    replyto = $('#reply_to').val();
    $.post('/api/post/add',{tid:tid,'content':content,'replyto':replyto},reply_callback,async=false);
}

function reply_ready() {
  $('#submit_reply').click(reply_thread);
}

$(document).ready(reply_ready);
