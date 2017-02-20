var page = 0;
var next_page, prev_page;
var reviews = document.getElementsByClassName('review');

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
