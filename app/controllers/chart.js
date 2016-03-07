'use strict';

angular.module('colornameHtmlApp')
  .controller('ChartCtrl', function($scope, $http, $routeParams) {
    var fetchJSON = function(fileName) {
      $http.get(fileName).success(function(response) {
        var chartData = {};
        for (var name in response) {
          var color = response[name];
          var red = color[0];
          var green = color[1];
          var blue = color[2];
          var colorHex = ((1 << 24) + (red << 16) + (green << 8) + blue).toString(16).substr(1);
          var isDark = (red + green + blue) / 3 < 128;
          chartData[name] = {
            "rgb": color,
            "hex": colorHex,
            "isDark": isDark
          }
        }
        $scope.chartData = chartData;
      });
    };
    var fileName = $routeParams.fileName;
    var filePath = "pycolorname/data/" + fileName;
    var fileNameToTitle = {
      "pycolorname.pantone.logodesignteam.json": "Pantone - LogoDesignTeam",
      "pycolorname.pantone.pantonepaint.json": "Pantone - PantonePaint",
      "pycolorname.pantone.cal_print.json": "Pantone - CalPrint",
      "pycolorname.ral.classic.ralcolor.json": "RAL - Classic - RALColor",
      "pycolorname.ral.classic.wikipedia.json": "RAL - Classic - Wikipedia"
    };
    fetchJSON(filePath);
    $scope.chartName = fileNameToTitle[fileName];
  });
