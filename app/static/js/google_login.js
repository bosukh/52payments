var auth2;

function signOut() {
  auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
}
function onSignIn(googleUser) {
  var id_token = googleUser.getAuthResponse().id_token;
  signOut();
  document.getElementById('id_token').value = id_token;
  document.getElementById('google-login-form').submit();
}
