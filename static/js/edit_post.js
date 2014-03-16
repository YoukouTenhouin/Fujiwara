function thread_callback(json){
    if (json['success']){
	window.location.pathname='/thread/view/'+tid+"#"+pid;
    } else {
	if (json['error'] == 1){
	    $('#edit_notlogin_alert').show();
	}
    }
}

function submit_post_update() {
    content =  $('#edit_form #content').val();
    $.post('/api/post/update',{'pid':pid,'content':content},thread_callback,async=false);
}



function post_update_ready() {
    $('#edit_form #submit').click(submit_post_update);
}

$(document).ready(post_update_ready);
