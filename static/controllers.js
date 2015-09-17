'use strict';

var controllers = angular.module('controllers', []);

controllers.controller('home_controller', ['$scope', '$location', 'db', 'spinner', function($scope, $location, db, spinner) {

	$scope.data = null;
	$scope.db = new db('summoners');
	$scope.spinner = new spinner();

	$scope.summoner = {'name': '', 'email': '', 'password': '', 'id': 0}


	$scope.list = function()
	{
		$scope.spinner.start();
		$scope.db.list()
			.success(function(data) {
				$scope.data = data;
				$scope.spinner.stop();
				console.log($scope.data);
			});
	}

	$scope.create = function()
	{
		$scope.db.create($scope.summoner)
			.success(function(data) {
				$scope.data.summoners.push(data);
				console.log(data);
			});
	}

	$scope.list();
}]);


controllers.controller('login_controller', ['$scope', '$rootScope', '$location', 'AuthenticationService', function($scope, $rootScope, $location, AuthenticationService) {

	AuthenticationService.ClearCredentials();

	$scope.send_login = function() {
		$scope.error = false;

		AuthenticationService.Login($scope.login, $scope.password, function(response) {
			if (response.success)
			{
				console.log(response);
				if (response.status == 404)
				{
					$scope.error = true;
				}
				else
				{
					AuthenticationService.SetCredentials(response.record.login, response.record.password);
					$location.path('/home/');
				}
			}
			else
			{
				$scope.error = true;
			}
		});
	};
}]);

controllers.controller('logout_controller', ['$scope', '$location', 'AuthenticationService', function($scope, $location, AuthenticationService) {
	AuthenticationService.ClearCredentials();
	$location.path('/login/');
}]);
