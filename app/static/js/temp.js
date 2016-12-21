var search = {};
search.get = function() {
  var url = '/get_all_companies';
  var xhr = create_xhr('GET', url, function(){
    sessionStorage.setItem('data', xhr.responseText);
    data = JSON.parse(sessionStorage.getItem('data'));
  });
  xhr.send();
};
search.get();
var criteria = sessionStorage.getItem('selected_item_list');
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
};
var includes_all = function(a, b){
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
};
var res = [];
for (let row of data){
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

res.sort(function(a, b) {
    return parseFloat(a.pricing_range[1]) - parseFloat(b.pricing_range[1]);
});
if (res.length == 0){
  var elem = document.createElement('h5');
  elem.innerHTML = 'No Matching Result';
  document.body.appendChild(elem);
}
//else
for (let row of data){
  
}
