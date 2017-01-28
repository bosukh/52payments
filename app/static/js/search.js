var types, search_criteria, current_type, items;
var selected_items, selected_item_list, clear_all_btn;
var featured_title = document.getElementById('featured-title');
var featured = document.getElementById('featured-companies');

function init_search_box() {
  init_vars();
  toggle_clear_all_btn();
  fill_items(types[current_type], items);
}
function init_vars(){
  clear_all_btn = document.getElementById('clear-all');
  items = document.getElementById('items');
  selected_items = document.getElementById('selected-items');
  search_criteria = document.getElementById('search_criteria');
  types = get_criteria_list();
  selected_item_list = get_selected_item_list();
  if (!current_type){
    current_type = "Pricing Method";
  };
}
function get_criteria_list(){
  if (sessionStorage.getItem('Business Types')){
    var biz_type = sessionStorage.getItem('Business Types').split(',');
  } else {
    var biz_type = ['Retail', 'Restaurant', 'E-Commerce',
                    'Healthcare/Medical', 'Mobile', 'Professional/Personal Services',
                    'Non-Profit', 'High-Risk', 'High-Volume', 'Other'];
  }
  if (sessionStorage.getItem('Complimentary Services')){
    var srv_type = sessionStorage.getItem('Complimentary Services').split(',');
  } else {
    var srv_type = ['Marketing', 'Analytics', 'Recurling Bill',
                    'Chargeback', 'Security', 'Other'];
  }
  if (sessionStorage.getItem('Equipments')){
    var equip_type = sessionStorage.getItem('Equipments').split(',');
  } else {
    var equip_type = ['Verifone', 'Ingenico', 'Other'];
  }
  if (sessionStorage.getItem('Pricing Method')){
    var pricing_type = sessionStorage.getItem('Pricing Method').split(',');
  } else {
    var pricing_type = ['Tiered', 'Interchange Plus', 'Flat', 'Custom'];
  }
  types = {
    "Business Types" : biz_type,
    "Complimentary Services" : srv_type,
    "Equipments" : equip_type,
    "Pricing Method" : pricing_type
  };
  return types;
}
function select_items_title(items_title){
  current_type = items_title.innerHTML;
  var items_titles = document.getElementsByClassName('items-title');
  for (var i = 0; i < items_titles.length; i++){
    items_titles[i].className = 'items-title';
  }
  items_title.className = 'items-title selected';
  var current_num = items.childNodes.length;
  for (var i = 1; i < current_num; i++){
    items.childNodes[1].remove();
  }
  fill_items(types[current_type], items);
}
function fill_items(list_, items, selected = 0){
  for (var i = 0; i < list_.length; i++){
    var item = document.createElement('button');
    item.className = 'item';
    if (selected){
      item.className = 'item selected-item';
      item.onclick = function(){deselect(this)};
      item.innerHTML = list_[i] + ' x';
    } else{
      item.setAttribute("id", list_[i]);
      item.onclick = function(){select(this)};
      item.innerHTML = list_[i];
    }
    items.appendChild(item);
  }
}
function select(item){
  pop(types[current_type], item.innerHTML);
  sessionStorage.setItem(current_type, types[current_type]);
  selected_item_list.push(current_type + ': '+ item.innerHTML);
  sessionStorage.setItem('selected_item_list', selected_item_list);
  fill_items([current_type + ': '+ item.innerHTML], selected_items, 1);
  item.remove();
  document.getElementById('chosen-title').style.opacity= 1;
  search_criteria.value = selected_item_list.join(',');
  toggle_clear_all_btn();
}
function deselect(item){
  var selected_item_name = item.innerHTML.trim();
  var type = selected_item_name.split(': ')[0];
  var item_name = selected_item_name.split(': ')[1].split(' x')[0];
  pop(selected_item_list, selected_item_name);
  sessionStorage.setItem('selected_item_list', selected_item_list);
  types[type].push(item_name);
  sessionStorage.setItem(current_type, types[current_type]);
  if (types[current_type].includes(item_name)){
    fill_items([item_name], items);
  }
  item.remove();
  if (selected_item_list.length == 0){
    document.getElementById('chosen-title').style.opacity= 0;
  }
  search_criteria.value = selected_item_list.join(',');
  toggle_clear_all_btn();
}
function get_selected_item_list(){
  if (sessionStorage.getItem('selected_item_list')){
    selected_item_list = sessionStorage.getItem('selected_item_list').split(',');
    document.getElementById('chosen-title').style.opacity= 1;
    fill_items(selected_item_list, selected_items, 1);
    search_criteria.value = selected_item_list.join(',');
  } else {
    selected_item_list = [];
  };
  return selected_item_list;
}
function toggle_clear_all_btn() {
  if (!selected_item_list || selected_item_list.length==0){
    clear_all_btn.style = 'display:none;'
  } else {
    clear_all_btn.style = 'display:block;'
  }
}
function get_search_result_base(func = 0) {
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
  };
  var url = '/search_results?' + 'search_criteria='+encodeURIComponent(search_criteria.value)
  var xhr = create_xhr('GET', url, after_todo);
  xhr.send();
  if (func) {
    func();
  }
}
function clear_search_criteria() {
  sessionStorage.clear();
  search_criteria.value = '';
  items.innerHTML = '';
  selected_items.innerHTML = ''
  document.getElementById('chosen-title').style.opacity= 0;
  init_search_box();
}
function get_search_result(){
  get_search_result_base(function() {
    featured_title.remove();
    featured.remove();
  });
}


init_search_box();
if (typeof(search_criteria)!='undefined' & search_criteria.value != ''){
  get_search_result();
} else {
  add_cont_reading_btn();
}
