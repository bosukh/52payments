var input_list = ['rating', 'title', 'content', 'first_name', 'last_name', 'email'];
var rating_input = document.getElementById('rating');
var rating_text = document.getElementById('rating_text');
var ratings = []

// require form_validation
function close_write_review(){
  document.getElementById('write-review-box').style = 'display: none;'
}
function check_all(){
  var bad = check_all_field(input_list, false);
  if (!bad){
    enable_btn('review-submit-button');
  } else {
    disable_btn('review-submit-button');
  }
}
function on_write_review() {
  document.getElementById('title').style = 'width:calc(100% - 8px);' ;
  document.getElementById('content').style = 'width:100%;';
  var width_ = document.getElementById('write-review-box').offsetWidth;
  document.getElementById('content').style = 'width: 100%; height:200px;'
  disable_btn('review-submit-button');
}
function show_review_box(){
  document.getElementById('write-review-box').style = 'display:block;';
  check_all();
}

document.getElementById('title').setAttribute('maxlength', '120')
document.getElementById('content').setAttribute('maxlength', '5000')
disable_btn('review-submit-button');
var temp = [];
for (var i = 0; i < input_list.length; i++){
  var elem = document.getElementById(input_list[i]);
  if (elem){
    elem.setAttribute('oninput', 'check_all()');
  } else {
    temp.push(input_list[i])
  }
}
for (a of temp){
  pop(input_list, a);
}
if (input_list.includes('email')){
  var elem = document.getElementById('email');
  var check_email = function(){
    check_input(elem, email_re);
    check_all();
  }
  var function_call = 'check_email()';
  elem.setAttribute('oninput', function_call);
}
hide_warnings(['email']);

rating_input.value = '';
for (var i=1; i< 6;i++){
  ratings.push(document.getElementById('rating_'+ i));
}
for (var i = 0; i < ratings.length; i++){
  var rating = ratings[i];
  rating.addEventListener('click', (function(rating, i){
    return function() {
      var rating_num = i+1;
      rating_input.value = rating_num;
      rating_text.innerHTML = rating_num;
      for (var j = 0; j < rating_num; j++){
        ratings[j].innerHTML = '★';
      }
      for (var q = rating_num; q < 5 ; q++){
        ratings[q].innerHTML = '☆';
      }
      check_all();
      };
  })(rating, i));
}

display_current_page(page, reviews);
add_cont_reading_btn();
