//var initialize = function(navigator) {
//	console.log(navigator);
//}

window.Superlists = {
	Accounts: {
		initialize: function (navigator) {
			$('#id_login').on('click', function () {
				navigator.id.request();
			});

			navigator.id.watch({
				loggedInUser: 'current user',
				onlogin: function(assertion) { 
					$.post(urls.login, { assertion: assertion, csrfmiddlewaretoken: token })
					 .done(function () { window.location.reload(); })
					 .fail(function () { navigator.id.logout(); }); 
				},
				onlogout: function () {}
			});
		}
	}
}