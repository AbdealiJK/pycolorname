'use strict';

angular
  .module('colornameHtmlApp', ['ngRoute'])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'app/views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/chart/:fileName', {
        templateUrl: 'app/views/chart.html',
        controller: 'ChartCtrl',
        controllerAs: 'chart'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
