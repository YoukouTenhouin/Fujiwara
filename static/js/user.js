var onlogin_callbacks = new Array();
var onlogout_callbacks = new Array();
window.user = null;

function update_nav_bar_login(user){
    $('#login_navbar').hide();
    $('#reg_navbar').hide();
    $('#nav_user_link span').text(user['name']);
    $('#nav_user').show();
}

function update_nav_bar_logout(){
    $('#nav_user').hide();
    $('#login_navbar').show();
    $('#reg_navbar').show();
}

function check_login(){
    $.getJSON('/api/user/info',function(json){
	if (json['logind']){
	    window.user = json;
	    for (var i in onlogin_callbacks){
		onlogin_callbacks[i](json);
	    }
	} else {
	    window.user = null;
	    for (var i in onlogout_callbacks) {
		onlogout_callbacks[i]();
	    }
	}
    },async=false);
}

function add_login_callback(callback){
    onlogin_callbacks.push(callback);
    if ( window.user != null ){
	callback(user);
    }
}

function add_logout_callback(callback){
    onlogout_callbacks.push(callback);
    if ( window.user == null ){
	callback();
    }
}

function reg_callback(json){
    if(json['success']){
	$('#exists_alert').hide();
	$('#not_filled_alert').hide();
	$('#reg_modal').modal('hide');
	check_login();
    } else {
	if(json['code'] == 1) {
	    $('#not_filled_alert').hide();
	    $('#exists_alert').show();
	}
	if(json['code'] == 2){
	    $('#exists_alert').hide();
	    $('#not_filled_alert').show();
	}
    }
}	

function register(){
    user = $('#reg_user').val();
    pwd = $('#reg_pwd').val();
    email = $('#reg_email').val();
    $.post('/api/user/register',{'user':user,'pwd':pwd,'email':email},reg_callback);
}

function login_callback(json){
    if(json['success']) {
	$('#login_alert').hide();
	$('#login_modal').modal('hide');
	check_login();
    } else {
	$('#login_alert').show();
    }
}

function login(){
    user = $('#login_user').val();
    pwd = $('#login_pwd').val();
    $.post('/api/user/login',{'user':user,'pwd':pwd},login_callback,async=false);
}

function user_ready(){
    check_login();
    
    add_login_callback(update_nav_bar_login);
    add_logout_callback(update_nav_bar_logout);
    
    $('#login_alert').hide();
    $('#exists_alert').hide();
    $('#not_filled_alert').hide();
    
    $('#submit_login').click(login);
    $('#submit_reg').click(register);

    $('#login_user').keyup(function(e){if(e.which == 13){$('#login_pwd').focus();}});
    $('#login_pwd').keyup(function(e){if(e.which == 13){login()}});

    $('#reg_email').keyup(function(e){if(e.which == 13){$('#reg_user').focus();}});
    $('#reg_user').keyup(function(e){if(e.which == 13){$('#reg_pwd').focus();}});
    $('#reg_pwd').keyup(function(e){if(e.which == 13){register();}});
    
    $('#login_navbar').click(function(){$('#login_modal').modal()});
    $('#reg_navbar').click(function(){$('#reg_modal').modal()});
    $('#logout_link').click(function(){$.post('/api/user/logout',check_login,async=false);});
}

$(document).ready(user_ready);