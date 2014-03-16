function thread_callback(json){
    if (json['success']){
	window.location.pathname='/thread/view/'+tid;
    } else {
	if (json['error'] == 1){
	    $('#edit_notlogin_alert').show();
	}
    }
}

function submit_thread_update() {
    title = $("#edit_form #title").val();
    tags = $("#edit_form #tags").val();
    $.post('/api/thread/update',{'tid':tid,'title':title,'tags':tags},thread_callback,async=false);
}



function thread_update_ready() {
    $('#edit_form #submit').click(submit_thread_update);
}

$(document).ready(thread_update_ready);
