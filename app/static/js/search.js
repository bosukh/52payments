var data = {};
var templates = {
  'header':`<div id = 'search-result-title' style = 'margin-top: 30px;' class="row">
    <div class="column">
      <h4>Search Results</h4>
    </div>
    <div class="column">
      <a style='float:right;' href="#">sort</a>
    </div>
  </div>
  {{^size}}
  <h5>No Matching Result</h5>
  {{/size}}`,
  'company':`<div style='padding:0px; margin:0px;' class="company-profile-container">
    <div class="search-result-left-col row">
      <div class="column">
        <img src="/img/{{company_profile_name}}" alt="company_logo" width="100%">
        <br><br>
        {{#pricing_range}}
        Pricing Range: {{lower_pricing_range}}% ~ {{upper_pricing_range}}%<br>
        {{/pricing_range}}
        Overall User Rating <br>
        {{#rounded_rating}}
        <span class='rating-star'>{{.}}</span>
        {{/rounded_rating}}
        {{avg_rating}} ({{num_ratings}}) <br>
        √ Verified With 52Payments <br>
      </div>
    </div>
    <div class="search-result-right-col row">
      <div style='padding-left:0px;' class="column">
        <a href="/company/{{company_profile_name}}">
          <button style = 'float:right;' id= 'company-profile-button' class= 'search-result-button button' type="button" name="button">View Full Profile</button>
        </a>
        <a href="{{landing_page}}">
          <button style = 'float:right;' id='company-apply-button' class= 'search-result-button button' type="button" name="button">Apply</button>
        </a>
        {{#title}}
        <h5 id='company-title'>{{title }}</h5>
        {{/title}}
        {{#pricing_method}}
        <b>Pricing Method</b>: {{pricing_method}}
        {{/pricing_method}}
        <br>
        {{#provided_srvs}}
        <b>Provided Services</b>: {{provided_srvs}}
        {{/provided_srvs}}
        <br><br>
        {{#summary}}
        <p>
          {{summary}}
        </p>
        {{/summary}}
      </div>
    </div>
  </div>
  <br><br>
  `
};
var search = {
    get_all: function(stop=0){
      if (stop==3){
        return false;
      }
      if (sessionStorage.getItem('data_all')){
        data.all = sessionStorage.getItem('data_all')
        return false;
      }
      var url = '/get_all_companies';
      var xhr = create_xhr('GET', url, function(){
        sessionStorage.setItem('data_all', xhr.responseText);
        data.all = JSON.parse(xhr.responseText);
        if (data.all.length == 0){
          stop++;
          window.setTimeout(search.get_all(stop), 100);
        }
      });
      xhr.onerror = function(){
        stop++;
        window.setTimeout(search.get_all(stop), 100);
      };
      xhr.send();
    },
    get_filter:function(){
      var criteria = sessionStorage.getItem('selected_item_list');
      if (!criteria){
        criteria = '';
      }
      criteria = criteria.split(',').map(function(a){return a.split(': ');});
      var search_filter = {
        'complementary_srvs':[],
        'equipment':[],
        'pricing_method':[],
        'provided_srvs':[]
      };
      for (var i = 0; i < criteria.length; i++){
        if (criteria[i][0] == "Complimentary Services"){
          search_filter['complementary_srvs'].push(criteria[i][1]);
        } else if (criteria[i][0] == "Business Types") {
          search_filter['provided_srvs'].push(criteria[i][1]);
        } else if (criteria[i][0] == "Pricing Method"){
          search_filter['pricing_method'].push(criteria[i][1]);
        } else if (criteria[i][0] == "Equipments") {
          search_filter['equipment'].push(criteria[i][1]);
        }
      }
      return search_filter;
    },
    includes_all: function(a,b){
      // if a includes all elem of b, return true
      if (b.length == 0){
        return true;
      }
      var count = 0;
      for (let elem of b){
        if (a.includes(elem)){
          count++;
        }
      }
      return count == b.length;
    },
    run_search: function(){
      var search_filter = search.get_filter();
      var not_empty = 0;
      for (let k in search_filter){
        if (search_filter.hasOwnProperty(k)){
          not_empty+= search_filter[k].length;
        }
      }
      if (!not_empty){
        return data.all;
      }
      var res = [];
      for (let row of data.all){
        var counter = 0;
        for (let k in search_filter){
          if (search_filter.hasOwnProperty(k)){
            if (!search.includes_all(row[k], search_filter[k])){
              counter++;
            }
          }
        }
        if (counter == 0){
          res.push(row);
        }
      }
      return res;
    },
    sort_by_num: function(res, col, desc=false){
      if (desc == true){
        res.sort(function(a, b) {
          return parseFloat(b[col]) - parseFloat(a[col]);
        });
      } else{
        res.sort(function(a, b) {
          return parseFloat(a[col]) - parseFloat(b[col]);
        });
      }
      return res;
    },
    render: function(col=false, desc=false){
      if (!data){
        window.setTimeout(search.render, 100);
      } else {
        if (!data.all){
          window.setTimeout(search.render, 100);          
        }
      }
      res_div.innerHTML = '';
      var res = search.run_search();
      var result = {
        'size': res.length
      };
      res_div.innerHTML+= Mustache.render(templates.header, result);
      search.toggle_loader();
      if (res.length == 0){
        return false;
      }
      if (col & col!='pricing_range'){
        res = sort_by_num(res, col, desc)
      } else if (desc==true & col == 'pricing_range'){
        res = res.sort(function(a, b) {
          return parseFloat(b.pricing_range[1]) - parseFloat(a.pricing_range[1]);
        });
      } else {
        res = res.sort(function(a, b) {
          return parseFloat(a.pricing_range[1]) - parseFloat(b.pricing_range[1]);
        });
      }
      for (let row of res){
        var company = Object.assign({}, row);
        var t = company.pricing_range;
        company.pricing_range = {
          'lower_pricing_range': (t[0]).toFixed(1),
          'upper_pricing_range': (t[1]).toFixed(1)
        };
        t = company.rounded_rating;
        var temp = []
        for (var i= 0; i < t; i++){
          temp.push('★');
        }
        for (var i= t; i < 5; i++){
          temp.push('☆');
        }
        company.rounded_rating = temp;
        company.avg_rating = company.avg_rating.toFixed(1);
        company.pricing_method = company.pricing_method.join(', ');
        company.provided_srvs = company.provided_srvs.join(', ');
        add_cont_reading_btn();
        adjust_height();
        res_div.innerHTML += Mustache.render(templates.company, company);
      }
    },
    toggle_loader: function(){
      if (loader_div.style.display== 'none'){
        loader_div.style.display = 'block';
      } else {
        loader_div.style.display = 'none';
      }
    }
};

function fill_items(list_, items, selected = 0){
  for (var i = 0; i < list_.length; i++){
    var item = document.createElement('button');
    item.className = 'item';
    if (selected){
      item.className = 'item selected-item';
      item.onclick = function(){deselect(this)};
    } else{
      item.setAttribute("id", list_[i]);
      item.onclick = function(){select(this)};
    };
    item.innerHTML = list_[i];
    items.appendChild(item);
  };
};
function select(item){
  featured_div.innerHTML = '';
  search.toggle_loader();
  pop(types[current_type], item.innerHTML);
  sessionStorage.setItem(current_type, types[current_type]);
  selected_item_list.push(current_type + ': '+ item.innerHTML);
  sessionStorage.setItem('selected_item_list', selected_item_list);
  fill_items([current_type + ': '+ item.innerHTML], selected_items, 1);
  document.getElementById('chosen-title').style.opacity= 1;
  search_criteria.value = selected_item_list.join(',');
  toggle_clear_all_btn();
  item.remove();
  search.render();
}
var deselect = function(item){
  search.toggle_loader()
  var selected_item_name = item.innerHTML.trim();
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
  toggle_clear_all_btn();
  search.render();
}
var select_items_title = function(items_title){
  current_type = items_title.innerHTML;
  var items_titles = document.getElementsByClassName('items-title');
  for (var i = 0; i < items_titles.length; i++){
    items_titles[i].className = 'items-title';
  };
  items_title.className = 'items-title selected';
  var current_num = items.childNodes.length
  for (var i = 1; i < current_num; i++){
    items.childNodes[1].remove();
  };
  fill_items(types[current_type], items);
}

var get_criteria_list = function(){
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
  types = {
    "Business Types" : biz_type,
    "Complimentary Services" : srv_type,
    "Equipments" : equip_type,
    "Pricing Method" : pricing_type
  }
  return types
}
var get_selected_item_list = function(){
  if (sessionStorage.getItem('selected_item_list')){
    selected_item_list = sessionStorage.getItem('selected_item_list').split(',');
    document.getElementById('chosen-title').style.opacity= 1;
    fill_items(selected_item_list, selected_items, 1);
    search_criteria.value = selected_item_list.join(',');
  } else {
    selected_item_list = [];
  };
  return selected_item_list
}

var init_vars = function(){
  clear_all_btn = document.getElementById('clear-all');
  items = document.getElementById('items');
  selected_items = document.getElementById('selected-items');
  search_criteria = document.getElementById('search_criteria');
  types = get_criteria_list();
  selected_item_list = get_selected_item_list();
  if (!current_type){
    current_type = "Business Types";
  };
}
var toggle_clear_all_btn = function() {
  if (!selected_item_list || selected_item_list.length==0){
    clear_all_btn.style = 'display:none;'
  } else {
    clear_all_btn.style = 'display:block;'
  };
}
var init_search_box = function() {
  init_vars();
  toggle_clear_all_btn();
  fill_items(types[current_type], items);
}

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
