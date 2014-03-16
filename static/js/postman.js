function hide_post(){
    pid = $(this).parents('.post_entry').data('post')._id;
    $.post('/api/post/del',{'pid':pid},function(){location.reload()},async=false);
}

function hide_thread(){
    $.post('/api/thread/del',{'tid':tid},function(){window.location.pathname='/'},async=false);
}

function postman_onlogin_callback(user){
    if(user['jobs'].indexOf('admin') != -1){
	$('#btn-hide-thread').show();
	$('.btn-hide-floor').show();
    }
}

function postman_onready(){
    add_login_callback(postman_onlogin_callback);
    add_logout_callback(postman_onlogout_callback);
    $('#btn-hide-thread').click(hide_thread);
    $('.btn-hide-floor').click(hide_post);
}

function postman_onlogout_callback(){
    $('#btn-hide-thread').hide();
    $('.btn-hide-floor').hide();
}

$(document).ready(postman_onready);
