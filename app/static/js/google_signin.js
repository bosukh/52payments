function onSignUp(googleUser) {
  var profile = googleUser.getBasicProfile();
  document.getElementById('id_token').value = googleUser.getAuthResponse().id_token;
  document.getElementById('email').value = profile.getEmail();
  document.getElementById('first_name').value = profile.getGivenName();
  document.getElementById('last_name').value = profile.getFamilyName();
  document.getElementById('signup-form').submit();
  signOut();
}
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  document.getElementById('id_token').value = googleUser.getAuthResponse().id_token;
  document.getElementById('email').value = profile.getEmail();
  document.getElementById('password').value =googleUser.getAuthResponse().id_token;
  document.getElementById('login-form').submit();
}
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  var id_token = googleUser.getAuthResponse().id_token;
  var email = profile.getEmail();
  var first_name = profile.getGivenName();
  var last_name = profile.getFamilyName();
  var onload = function() {
    console.log('Signed in as: ' + xhr.responseText);
    window.location.href = "/index";
  };
  var xhr = create_xhr('POST', '/tokensignin', onload);
  xhr.send('idtoken=' + id_token + '&email='+email + '&first_name='+first_name+ '&last_name='+last_name);
}
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
}
