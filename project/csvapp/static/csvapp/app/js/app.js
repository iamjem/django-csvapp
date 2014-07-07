'use strict';


angular.module('app', [
  'ngRoute',
  'ngCookies',
  'angularFileUpload',
  'app.services',
  'app.controllers'
])
.value('MEDIA_URL', MEDIA_URL)
.value('documentEndpoint', '/api/documents/')
.value('sortedDocumentEndpoint', '/api/sorted-document/')
.config(['$routeProvider', function($routeProvider) {
  $routeProvider
    .when('/', {
        templateUrl: STATIC_ROOT + 'views/main.html', 
        controller: 'MainCtrl'
    })
    .when('/document/:id', {
        templateUrl: STATIC_ROOT + 'views/document.html', 
        controller: 'DocumentCtrl'
    })
    .otherwise({
        redirectTo: '/'
    });
}])
.run(['$http', '$cookies', function($http, $cookies){
    // add CSRF headers for AJAX...
    // really should have something more sophisticated to make sure
    // this wouldn't get included in cross site AJAX requests
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
}]);
