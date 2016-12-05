var auth2;
function signOut() {
  auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
}

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  var id_token = googleUser.getAuthResponse().id_token;
  var email = profile.getEmail();
  var first_name = profile.getGivenName();
  var last_name = profile.getFamilyName();
  var onload = function() {
    signOut();
    if (xhr.responseText.length > 1){
      alert(xhr.responseText);
      if (xhr.responseText == 'Successfully registered. Please login.') {
        window.location.replace("/login");        
      };
    } else{
      window.location.replace("/index");
    };
  }
  var xhr = create_xhr('POST', '/google_signin', onload);
  xhr.send('id_token=' + id_token + '&last_name='+last_name + '&first_name='+first_name);
}
