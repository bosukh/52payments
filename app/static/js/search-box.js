var fill_items = function(list_, items, selected = 0){
  for (var i = 0; i < list_.length; i++){
    var item = document.createElement('div');
    item.className = 'item';
    if (selected){
      item.className = 'item selected-item';
      item.innerHTML = list_[i] + ' <span style="font-weight:bold;"><a class="items-title" onclick="javascript:deselect(this)">×</a></span>';
    } else{
      item.setAttribute("id", list_[i]);
      item.innerHTML = '<a class="items-title" onclick="javascript:select(this)">' + list_[i] + '</a>';
    };
    items.appendChild(item);
  };
}
var select = function(item){
  pop(types[current_type], item.innerHTML);
  sessionStorage.setItem(current_type, types[current_type]);
  selected_item_list.push(current_type + ': '+ item.innerHTML);
  sessionStorage.setItem('selected_item_list', selected_item_list);
  fill_items([current_type + ': '+ item.innerHTML], selected_items, 1);
  item.parentElement.remove();
  document.getElementById('chosen-title').style.opacity= 1;
  search_criteria.value = selected_item_list.join(',');
}
var deselect = function(item){
  var item = item.parentElement.parentElement;
  var selected_item_name = item.innerHTML.split('<span')[0].trim();
  var type = selected_item_name.split(': ')[0];
  var item_name = selected_item_name.split(': ')[1];
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
  };
  search_criteria.value = selected_item_list.join(',');
}
var select_items_title = function(items_title){
  current_type = items_title.innerHTML;
  items_title = items_title.parentElement;
  var items_titles = document.getElementsByClassName('items-title-div');
  for (var i = 0; i < items_titles.length; i++){
    items_titles[i].className = 'items-title-div';
  };
  items_title.className = 'selected items-title-div'
  var current_num = items.childNodes.length
  for (var i = 1; i < current_num; i++){
    items.childNodes[1].remove();
  };
  fill_items(types[current_type], items);
}

if (sessionStorage.getItem('Business Types')){
  var biz_type = sessionStorage.getItem('Business Types').split(',');
} else {
  var biz_type = ['Retail', 'Restaurant', 'E-Commerce',
                  'Healthcare/Medical', 'Mobile', 'Professional/Personal Services',
                  'Non-Profit', 'High-Risk', 'High-Volume', 'Other'];
};
if (sessionStorage.getItem('Complimentary Services')){
  var srv_type = sessionStorage.getItem('Complimentary Services').split(',');
} else {
  var srv_type = ['Marketing', 'Analytics', 'Recurling Bill',
                  'Chargeback', 'Security', 'Other'];
};
if (sessionStorage.getItem('Equipments')){
  var equip_type = sessionStorage.getItem('Equipments').split(',');
} else {
  var equip_type = ['Verifone', 'Ingenico', 'Other'];
};
if (sessionStorage.getItem('Pricing Method')){
  var pricing_type = sessionStorage.getItem('Pricing Method').split(',');
} else {
  var pricing_type = ['Tiered', 'Interchange Plus',
                      'Flat', 'Custom'];
};
var types = {
  "Business Types" : biz_type,
  "Complimentary Services" : srv_type,
  "Equipments" : equip_type,
  "Pricing Method" : pricing_type
}
var search_criteria = document.getElementById('search_criteria');
var current_type = "Business Types";
var items = document.getElementById('items');
var selected_items = document.getElementById('selected-items');
if (sessionStorage.getItem('selected_item_list')){
  var selected_item_list = sessionStorage.getItem('selected_item_list').split(',');
  document.getElementById('chosen-title').style.opacity= 1;
  fill_items(selected_item_list, selected_items, 1);
  search_criteria.value = selected_item_list.join(',');
} else {
  var selected_item_list = [];
};

fill_items(biz_type, items);
