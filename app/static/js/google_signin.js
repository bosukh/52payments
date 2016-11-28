function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  document.getElementById('id_token').value = googleUser.getAuthResponse().id_token;
  document.getElementById('email').value = profile.getEmail();
  document.getElementById('first_name').value = profile.getGivenName();
  document.getElementById('last_name').value = profile.getFamilyName();
  document.getElementById('signup-form').submit();
}
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
    window.location.href = "/signout"
  });
}
