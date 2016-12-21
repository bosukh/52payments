var res_div = document.getElementById('search-result');
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
            if (!includes_all(row[k], search_filter[k])){
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
      }
      res_div.innerHTML == '';
      var res = search.run_search();
      var result = {
        'size': res.length
      };
      res_div.innerHTML+= Mustache.render(templates.header, result);
      if (res.length == 0){
        return false;
      }
      if (col & col!='pricing_range'){
        sort_by_num(res, col, desc)
      } else if (desc==true & col == 'pricing_range'){
        res.sort(function(a, b) {
          return parseFloat(b.pricing_range[1]) - parseFloat(a.pricing_range[1]);
        });
      } else {
        res.sort(function(a, b) {
          return parseFloat(a.pricing_range[1]) - parseFloat(b.pricing_range[1]);
        });
      }
      for (let row of data.all){
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
        res_div.innerHTML += Mustache.render(templates.company, company);
      }
    }
};
search.get_all();
