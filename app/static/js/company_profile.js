var input_list = ['rating', 'title', 'content'];
var rating_input = document.getElementById('rating');
var rating_text = document.getElementById('rating_text');
var ratings = []
var page = 0;
var next_page, prev_page;
var reviews = document.getElementsByClassName('review');

function close_write_review(){
  document.getElementById('write-review-box').style = 'display: none;'
}
function check_all(){
  var bad = check_all_field(input_list);
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
for (var i = 0; i < input_list.length; i++){
  var elem = document.getElementById(input_list[i]);
  elem.setAttribute('oninput', 'check_all()');
}
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