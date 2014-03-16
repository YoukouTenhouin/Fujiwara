function thread_callback(json){
  if (json['success']){
    window.location.pathname='/thread/view/'+json['tid'];
  } else {
    if (json['error'] == 1){
      $('#thread_notitle_alert').hide();
      $('#thread_notlogin_alert').show();
    }
    if(json['error'] == 2){
      $('#thread_notlogin_alert').hide();
      $('#thread_notitle_alert').show();
    }
  }
}

function submit_thread() {
    title = $('#new_thread_form #title').val();
    tags = $('#new_thread_form #tags').val();
    content =  $('#new_thread_form textarea').val();
    $.post('/api/thread/add',{'title':title,'tags':tags,'content':content},thread_callback,async=false);
}

function thread_ready() {
  $('#submit').click(submit_thread);
}

$(document).ready(thread_ready);
