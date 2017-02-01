var text_re = /^[a-zA-Z']+$/;
var email_re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
var phone_re = /^[0-9]+$/;
var password_re = /[a-zA-Z0-9!@#\$%\^&\*]{8,}$/
var field_ids = [];
var p_tags;
var p_tags_trimmed_parts = {};
var auth2;

var alert_login_required = function(){
  alert('You need to log-in.')
}
function signOut() {
  auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
}

function onSignIn(googleUser) {
  var id_token = googleUser.getAuthResponse().id_token;
  signOut();
  document.getElementById('id_token').value = id_token;
  document.getElementById('google-login-form').submit();
}
function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}
function pop(list_, item){
  var index = list_.indexOf(item);
  list_.splice(index, 1);
}
function hide_warnings(field_ids){
  for (var i = 0; i < field_ids.length; i++){
    document.getElementById('warning_'+field_ids[i]).style.display = 'none';
  };
};
function enable_btn(dom_id){
  var elem = document.getElementById(dom_id);
  elem.disabled = false;
  elem.style.opacity = 1;
};
function disable_btn(dom_id){
  var elem = document.getElementById(dom_id);
  elem.disabled = true;
  elem.style.opacity = 0.5;
};
function add_validator(dom_id, re_name){
  var elem = document.getElementById(dom_id);
  var function_call = 'check_input(this,' + re_name + ')'
  elem.setAttribute('oninput', function_call);
};
function check_all_field(field_ids, warnings = false){
  var bad = 0;
  for (var i = 0; i < field_ids.length; i++){
    if (warnings){
      if (document.getElementById('warning_'+field_ids[i]).style.display != 'none'|| document.getElementById(field_ids[i]).value == ''){
        bad = 1;
      };
    } else {
      if (document.getElementById(field_ids[i]).value == ''){
        bad = 1;
      };
    };
  };
  return bad == 1
};

function all_required_field_warning(bad){
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
function toggle_warning(bool_, message){
  if (bool_){
    message.style.display = 'none';
  } else {
    message.style.display = 'block';
  };
};
function check_input(elem, re) {
  var input = elem.value;
  var message = document.getElementById("warning_"+elem.id);
  toggle_warning(input.match(re), message);
  var all_warning = check_all_field(field_ids, true);
  all_required_field_warning(all_warning);
};

function create_xhr(method, url, func){
  var xhr = new XMLHttpRequest();
  xhr.open(method, url);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = func;
  return xhr
}
function cont_reading(a_tag, index){
  a_tag.remove();
  var temp = p_tags[index].innerHTML;
  p_tags[index].innerHTML =  temp + p_tags_trimmed_parts[index];
  if (typeof(adjust_height) != 'undefined'){
    adjust_height();
  };
};
function add_cont_reading_btn(){
  p_tags = document.querySelectorAll("[class^='trim']");
  p_tags_trimmed_parts = {};
  for (var i = 0; i < p_tags.length; i++){
    var char_num;
    for (class_name of p_tags[i].classList){
      if (class_name.slice(0, 4) == 'trim'){
        char_num = parseInt(class_name.split('-')[1]);
      }
    }
    if (char_num == undefined){
      char_num = 300;
    }
    text = p_tags[i].innerHTML.trim();
    if (text.length > char_num) {
      var front = text.slice(0, char_num);
      var back = text.slice(char_num);
      if (back[0]!=' ' & front[front.length-1] !=' '){
        var temp = front.split(' ');
        front = temp.slice(0, temp.length - 1).join(' ');
        back = temp[temp.length-1] + back;
      }
      p_tags_trimmed_parts[i] = back;
      p_tags[i].innerHTML = front + ' ';
      var cont_reading_btn = document.createElement('a');
      cont_reading_btn.className = 'cont_reading_btn';
      cont_reading_btn.setAttribute('onclick', 'cont_reading(this, '+ i +')');
      cont_reading_btn.innerHTML = 'Continue Reading';
      p_tags[i].appendChild(cont_reading_btn);
    }
  }
}
function hide_all(reviews){
  for (var i = 0; i < reviews.length; i++){
    reviews[i].style.display = 'none';
  };
}
function create_page_moves(page, reviews){
  next_page = page+1;
  prev_page = page-1;
  var next = document.getElementById('next');
  next.setAttribute('href', 'javascript:display_current_page(next_page, reviews)');
  next.style.display = 'none';
  var prev = document.getElementById('prev');
  prev.setAttribute('href', 'javascript:display_current_page(prev_page, reviews)');
  prev.style.display = 'none';
  if (page != 0){
    prev.style.display = 'inline-block';
  }
  if (reviews.length/3 > page+1){
    next.style.display = 'inline-block';
  }
}
function display_current_page(page, reviews){
  hide_all(reviews);
  for (var i = page*3; i < (page+1)*3 && i < reviews.length; i++){
    reviews[i].style.display = 'block';
  }
  create_page_moves(page, reviews);
}
