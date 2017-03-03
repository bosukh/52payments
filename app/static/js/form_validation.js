var text_re = /^[a-zA-Z']{1,}$/;
var email_re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
var phone_re = /^[0-9]{10,11}$/;
var password_re = /[a-zA-Z0-9!@#\$%\^&\*]{8,}$/
var field_ids = [];
var button_id, all_warning_id;

function hide_warnings(field_ids){
  for (var i = 0; i < field_ids.length; i++){
    document.getElementById('warning_'+field_ids[i]).style.display = 'none';
  }
}
function enable_btn(dom_id){
  var elem = document.getElementById(dom_id);
  elem.disabled = false;
  elem.style.opacity = 1;
}
function disable_btn(dom_id){
  var elem = document.getElementById(dom_id);
  elem.disabled = true;
  elem.style.opacity = 0.5;
}
function add_validator(dom_id, re_name){
  var elem = document.getElementById(dom_id);
  var function_call = 'check_input(this,' + re_name + ')'
  elem.setAttribute('oninput', function_call);
}
function check_all_field(field_ids, have_warnings_ = true){
  var bad = 0;
  for (var i = 0; i < field_ids.length; i++){
    if (have_warnings_){
      if (document.getElementById('warning_'+field_ids[i]).style.display != 'none'|| document.getElementById(field_ids[i]).value.trim() == ''){
        bad = 1;
      }
    } else{
      if (document.getElementById(field_ids[i]).value.trim() == ''){
        bad = 1;
      }
    }
  }
  return bad == 1;
}
function all_required_field_warning(bad){
  if (bad){
    if (typeof(all_warning_id) != "undefined"){
      document.getElementById(all_warning_id).style.display = 'block';
    }
    if (typeof(button_id) != "undefined"){
      disable_btn(button_id);
    }
  } else {
    if (typeof(all_warning_id) != "undefined"){
      document.getElementById(all_warning_id).style.display = 'none';
    }
    if (typeof(button_id) != "undefined"){
      enable_btn(button_id);
    }
  }
}
function toggle_warning(bool_, message){
  if (bool_){
    message.style.display = 'none';
  } else {
    message.style.display = 'block';
  }
}
function check_input(elem, re) {
  var input = elem.value;
  var message = document.getElementById("warning_"+elem.id);
  if (!input){
    toggle_warning(false, message);
  } else if (parseInt(re)) {
    toggle_warning(input.length >= parseInt(re), message);
  }else{
    toggle_warning(input.match(re), message);
  }
  var all_warning = check_all_field(field_ids);
  all_required_field_warning(all_warning);
}
