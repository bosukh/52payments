var p_tags;
var p_tags_trimmed_parts = {};

function alert_login_required(){
  alert('Please log-in');
}
function session_store(name, items_list){
  sessionStorage.setItem(name, items_list);
}
function sticky_note(term){
  var s_term = term.trim().toLowerCase();
  var note = glossary[s_term];
  if (!note){
    note = glossary[s_term+ 's'];
  }
  if (!note){
    return term;
  } else {
      return `
        ${term}
        <p class="hover_message">
          ${note}
        </p>
      `
    }
}
function show_hover_message(current){
  current.style = 'text-decoration:none;'
  for (node of current.children){
    if (node.className == 'hover_message'){
      node.style='display:block';
    }
  }
}
function hide_hover_message(current){
  current.style = 'text-decoration:underline;'
  for (node of current.children){
    if (node.className == 'hover_message'){
      node.style='display:none';
    }
  }
}

function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}

function pop(list_, item){
  var index = list_.indexOf(item);
  list_.splice(index, 1);
}

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
