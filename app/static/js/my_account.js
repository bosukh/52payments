var field_ids = ['first_name', 'last_name', 'email'];
var non_required_field_ids = ['first_name', 'last_name', 'email', 'phone'];
var button_id = 'save-button';
hide_warnings(non_required_field_ids);
var account = {
  hide_fields:function(){
    for (var k in account.input_fields){
      if (account.input_fields.hasOwnProperty(k)){
        account.input_fields[k].style.display = 'none';
      }
    }
  },
  submit_verify_email:function(){
    document.getElementById('verify_email').value = document.getElementById('user-email').innerHTML;
    document.getElementById('verify-email-form').submit();
  },
  get_vars:function(){
    account.fields = ['first_name', 'last_name', 'email', 'phone', 'company_name'];
    account.input_fields = {};
    account.infos = {};
    for (let k of account.fields){
      account.input_fields[k] = document.getElementById(k);
      account.infos[k] = document.getElementById('user-'+k);
    }
    account.edit_btn = document.getElementById('edit-button');
    account.edit_form = document.getElementById('edit_info_form');
    account.save_btn = document.getElementById('save-button');
    account.cancel_btn = document.getElementById('cancel-button');
    account.email_verify = document.getElementById('email-verify-div');
  },
  edit_info:function(){
    account.email_verify.style.display = 'none';
    account.edit_btn.style.display = 'none';
    account.save_btn.style.display = '';
    account.cancel_btn.style.display = '';
    for (var k in account.infos){
      if (account.infos.hasOwnProperty(k)){
        if (!account.infos[k]){
        } else {
          if (account.infos[k].innerHTML != 'None'){
            account.input_fields[k].value = account.infos[k].innerHTML;
          }
          account.infos[k].style.display='none';
          account.input_fields[k].style.display = '';
        }
      }
    }
    add_validator('first_name', 'text_re');
    add_validator('last_name', 'text_re');
    add_validator('email', 'email_re');
    add_validator('phone', 'phone_re');
  },
  cancel_edit: function(){
    account.email_verify.style.display = '';
    account.edit_btn.style.display = '';
    account.save_btn.style.display = 'none';
    account.cancel_btn.style.display = 'none';
    hide_warnings(non_required_field_ids);
    for (k in account.infos){
      if (account.infos.hasOwnProperty(k)){
        if (!account.infos[k]){
        } else {
          account.infos[k].style.display='';
          account.input_fields[k].style.display='none';
        }
      }
    }
  },
  save_edit:function(){
    if (document.getElementById('save-button').disabled){
      return;
    }
    account.email_verify.style.display = '';
    account.edit_btn.style.display = '';
    account.save_btn.style.display = 'none';
    account.cancel_btn.style.display = 'none';
    account.edit_form.submit();
  },
  toggle_edit_btn:function(){
    account.get_vars();
    if (account.edit_btn.lower() == 'edit') {
      account.edit_info();
    } else {
    }
  }
};
account.get_vars();
account.hide_fields();
var page = 0;
var next_page, prev_page;
var reviews = document.getElementsByClassName('review');
add_cont_reading_btn();
display_current_page(page, reviews);
