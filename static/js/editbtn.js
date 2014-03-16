function postedit_login_callback(user){
    if(window.user['_id'] == author_id) $('#btn-edit-thread').show();
    $('.btn-edit-post').each(function(){
	if($(this).parents('.post_entry').data()['author']._id == window.user['_id']) {
	    $(this).show();
	}
    });
}

function postedit_logout_callback(){
    $('.btn-edit-post').hide();
    $('#btn-edit-thread').hide();
}

function editbtn_ready(){
    add_login_callback(postedit_login_callback);
    add_logout_callback(postedit_logout_callback);
}

$(document).ready(editbtn_ready);
