var text_re = /^[a-zA-Z']+$/;
var email_re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
var phone_re = /^[0-9]+$/;
var password_re = /[a-zA-Z0-9!@#\$%\^&\*]{8,}$/
var field_ids = [];

function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}
var pop = function(list_, item){
  var index = list_.indexOf(item);
  list_.splice(index, 1);
}

var hide_warnings = function(field_ids){
  for (var i = 0; i < field_ids.length; i++){
    document.getElementById('warning_'+field_ids[i]).style.display = 'none';
  };
};

var enable_btn = function(dom_id){
  var elem = document.getElementById(dom_id);
  elem.disabled = false;
  elem.style.opacity = 1;
};
var disable_btn = function(dom_id){
  var elem = document.getElementById(dom_id);
  elem.disabled = true;
  elem.style.opacity = 0.5;
};

var add_validator = function(dom_id, re_name){
  var elem = document.getElementById(dom_id);
  var function_call = 'func(' + dom_id + ',' + re_name + ')'
  elem.setAttribute('oninput', function_call);
};

var check_all_field = function(field_ids){
  var bad = 0;
  for (var i = 0; i < field_ids.length; i++){
    if (document.getElementById('warning_'+field_ids[i]).style.display != 'none'|| document.getElementById(field_ids[i]).value == ''){
      bad = 1
    };
  };
  return bad == 1
};

var all_required_field_warning = function(bad){
  if (bad){
    if (typeof(all_warning_id) != "undefined"){
      document.getElementById(all_warning_id).style.display = 'block';
    };
    if (typeof(button_id) != "undefined"){
      disable_btn(button_id);
    }
  } else {
    if (typeof(all_warning_id) != "undefined"){
      document.getElementById(all_warning_id).style.display = 'none';
    };
    if (typeof(button_id) != "undefined"){
      enable_btn(button_id);
    }
  };
};

var toggle_warning = function(bool_, message){
  if (bool_){
    message.style.display = 'none';
  } else {
    message.style.display = 'block';
  };
};

var func = function(elem, re) {
  var input = elem.value;
  var message = document.getElementById("warning_"+elem.id);
  toggle_warning(input.match(re), message);
  var all_warning = check_all_field(field_ids);
  all_required_field_warning(all_warning);
};


var create_xhr = function(method, url, func){
  var xhr = new XMLHttpRequest();
  xhr.open(method, url);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = func;
  return xhr
}
