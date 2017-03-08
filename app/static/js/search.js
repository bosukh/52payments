var model = {};
function init_search_box() {
  init_cont.init_vars();
  cont.update_search_criteria(model.selected_item_list);
  view.toggle_clear_all_btn();
  view.fill_items_in_div(model.types[model.current_type], model.items,0);
  view.fill_items_in_div(model.selected_item_list, model.selected_items, 1);
}
function select_items_title(items_title){
  cont.update_current_type(items_title.id);
  view.render_selected_items_title(items_title);
}
var init_cont = {
  init_vars: function(){
    model.clear_all_btn = document.getElementById('clear-all');
    model.items = document.getElementById('items');
    model.items_titles = document.getElementsByClassName('items-title');
    model.featured_title = document.getElementById('featured-title');
    model.featured_comapnies = document.getElementById('featured-companies');
    model.selected_items = document.getElementById('selected-items');
    model.search_criteria = document.getElementById('search_criteria');
    model.types = init_cont.get_criteria_list();
    model.selected_item_list = init_cont.get_selected_item_list();
    if (!model.current_type){
      model.current_type = "Pricing_Methods";
    }
  },
  get_selected_item_list: function(){
    if (sessionStorage.getItem('selected_item_list')){
      selected_item_list = sessionStorage.getItem('selected_item_list').split(',');
    } else {
      selected_item_list = [];
    }
    return selected_item_list;
  },
  get_criteria_list: function(){
    if (sessionStorage.getItem('Business_Types')){
      var biz_type = sessionStorage.getItem('Business_Types').split(',');
    } else {
      var biz_type = ['E-Commerce', 'Enterprise', 'High-Risk',
                      'Mobile', 'Non-Profit', 'Professional/Personal Services',
                      'Restaurant', 'Retail', 'Other'];
    }
    if (sessionStorage.getItem('Complementary_Services')){
      var srv_type = sessionStorage.getItem('Complementary_Services').split(',');
    } else {
      var srv_type = ['ACH', 'Analytics/Reporting', 'Chargeback', 'Digital Wallet',
                      'Fraud', 'Inventory Management', 'Loyalty Program',
                      'Recurring Billing', 'Security', 'Other'];
    }
    if (sessionStorage.getItem('Terminals')){
      var equip_type = sessionStorage.getItem('Terminals').split(',');
    } else {
      var equip_type = ['Mobile Terminal', 'POS Solution', 'Terminal',
                        'Virtual/Gateway', 'Wireless Terminal', 'Other'];
    }
    if (sessionStorage.getItem('Pricing_Methods')){
      var pricing_type = sessionStorage.getItem('Pricing_Methods').split(',');
    } else {
      var pricing_type = ['Flat', 'Interchange Plus', 'Tiered', 'Custom', 'Other'];
    }
    var types = {
      "Business_Types" : biz_type,
      "Complementary_Services" : srv_type,
      "Terminals" : equip_type,
      "Pricing_Methods" : pricing_type
    };
    return types;
  }
}
var cont = {
  add_to_types:function(type_name, item_id){
    model.types[type_name].push(item_id);
  },
  remove_from_types: function(type_name, item_id){
    pop(model.types[type_name], item_id);
  },
  update_search_criteria: function(){
    model.search_criteria.value = model.selected_item_list.join(',');
  },
  update_current_type : function(name_of_type){
    model.current_type = name_of_type;
  },
  add_selected_item_list: function(item_id){
    selected_item_list.push(model.current_type + ': '+ item_id);
    session_store('selected_item_list', model.selected_item_list);
  },
  remove_selected_item_list: function(item_id){
    pop(model.selected_item_list, item_id);
    session_store('selected_item_list', model.selected_item_list);
  }

}
var view = {
  empty_div:function(items_div){
    var current_num = items_div.childNodes.length;
    for (var i = 0; i < current_num; i++){
      items_div.childNodes[0].remove();
    }
  },
  fill_items_in_div: function(item_list, items_div, selected){
    for (var i = 0; i < item_list.length; i++){
      var item = document.createElement('button');
      item.className = 'item';
      item.setAttribute("id", item_list[i]);
      if (selected){
        document.getElementById('chosen-title').style.opacity= 1;
        item.className = 'item selected-item';
        item.onclick = function(){deselect(this);hide_hover_message(this);};
        var name = item_list[i].split(': ')
        item.innerHTML =name[0] + ": " + sticky_note(name[1]) + ' x';
      }else{
        if (model.selected_item_list.length == 0){
          document.getElementById('chosen-title').style.opacity= 0;
        }
        item.onclick = function(){select(this);hide_hover_message(this);};
        item.innerHTML = sticky_note(item_list[i]);
      }
      item.onmouseleave=function(){hide_hover_message(this);};
      item.onmousecenter = function(){show_hover_message(this);};
      item.onmouseover = function(){show_hover_message(this);};
      items_div.appendChild(item);
    }
  },
  render_selected_items_title: function(items_title){
    for (var i = 0; i < model.items_titles.length; i++){
      model.items_titles[i].className = 'items-title';
    }
    items_title.className = 'items-title selected';
    view.empty_div(model.items);
    view.fill_items_in_div(model.types[model.current_type], model.items, 0);
  },
  toggle_clear_all_btn: function() {
    if (!model.selected_item_list || model.selected_item_list.length==0){
      model.clear_all_btn.style = 'display:none;';
    } else {
      model.clear_all_btn.style = 'display:block;';
    }
  }
}
function clear_search_criteria() {
  sessionStorage.clear();
  model.search_criteria.value = '';
  model.items.innerHTML = '';
  model.selected_items.innerHTML = ''
  document.getElementById('chosen-title').style.opacity= 0;
  init_search_box();
}
function select(item){
  cont.remove_from_types(model.current_type, item.id);
  session_store(model.current_type, model.types[model.current_type]);
  cont.add_selected_item_list(item.id);
  view.fill_items_in_div([model.current_type + ': '+item.id], model.selected_items, 1);
  item.remove();
  cont.update_search_criteria();
  view.toggle_clear_all_btn();
}
function deselect(item){
  var selected_item_name = item.id.trim();
  var type = selected_item_name.split(': ')[0];
  var item_name = selected_item_name.split(': ')[1].split(' x')[0];
  cont.add_to_types(type, item_name);
  cont.remove_selected_item_list(item.id);
  session_store(model.current_type, model.types[type]);
  if (model.types[model.current_type].includes(item_name)){
    view.fill_items_in_div([item_name], model.items,0);
  }
  item.remove();
  cont.update_search_criteria();
  view.toggle_clear_all_btn();
}
function get_search_result_base(func) {
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
  var url = '/search-results'
  var xhr = create_xhr('POST', url, after_todo);
  xhr.send('search_criteria='+model.search_criteria.value);
  if (func) {
    func();
  }
}
function get_search_result(){
  get_search_result_base(function() {
    model.featured_title.remove();
    model.featured_comapnies.remove();
  });
}
