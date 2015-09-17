'use strict';

var app = angular.module('app', [
	'ngRoute',
	'ngCookies',
	'controllers',
	'services',
	'timer'
]);

app.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/home/', {
			templateUrl: 'partials/home.tpl.html',
		})
		.when('/cadastro/', {
			templateUrl: 'partials/signup.tpl.html',
		})
		.when('/entrar/', {
			templateUrl: 'partials/login.tpl.html',
		})
		.when('/', {
			redirectTo: '/home/'
		})
		.otherwise({
			redirectTo: '/home/'
		});
}])

.run(['$rootScope', '$location', '$cookieStore', '$http',
		function($rootScope, $location, $cookieStore, $http) {
			$rootScope.globals = $cookieStore.get('globals') || {};
			if ($rootScope.globals.currentUser) {
				$http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata;
			}
}]);
