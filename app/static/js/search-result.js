var adjust_height = function(){
  var left_cols = document.getElementsByClassName('search-result-left-col');
  var right_cols = document.getElementsByClassName('search-result-right-col');
  if (left_cols.length) {
    for (var i = 0; i < left_cols.length; i++){
      if (left_cols[i].offsetHeight < right_cols[i].offsetHeight){
        left_cols[i].style.height =  right_cols[i].offsetHeight + 'px';
      };
    };
  };
}
var get_search_result_base = function(func = 0) {
  document.getElementById('loader').style = 'display: block;'
  var after_todo = function(){
    if (document.getElementById('search-result')){
      document.getElementById('search-result').innerHTML = xhr.responseText;
    }else{
      var elem = document.createElement('div');
      elem.setAttribute('id', 'search-result');
      elem.innerHTML = xhr.responseText;
      document.getElementById('content-container').appendChild(elem);
    }
    document.getElementById('loader').style = 'display: none;'
    add_cont_reading_btn();
    adjust_height();
  }
  var url = '/search_results?' + 'search_criteria='+encodeURIComponent(search_criteria.value)
  xhr = create_xhr('GET', url, after_todo);
  xhr.send();
  if (func) {
    func();
  };
}
