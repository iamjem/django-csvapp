'use strict';


angular.module('app.controllers', [])

.controller('MainCtrl', ['$scope', 'csvSocket', 'documentRepository', 'MEDIA_URL', function($scope, socket, repo, MEDIA_URL) {
    $scope.MEDIA_URL = MEDIA_URL;
    $scope.STATUS = {
        WAITING: 0,
        UPLOADING: 1,
        AWAITING: 2, // awaiting socketio message
        HAS_META: 3,
        ERROR: 4
    };

    $scope.uploadState = $scope.STATUS.WAITING;
    $scope.progress = 0;

    // spits out duplicate metadata
    var onSocketDocument = function(data){
        $scope.docmentMeta = data;
        $scope.uploadState = $scope.STATUS.HAS_META;
        $scope.$apply();
        $scope.refresh();
    };
    socket.on('document', onSocketDocument);

    // handle upload files
    $scope.onFileSelect = function(files){
        if ($scope.uploadState !== 0) return;
        $scope.progress = 0;
        $scope.uploadState = $scope.STATUS.UPLOADING;

        var promise = repo.create(files[0]);

        promise.progress(function(evt){
            $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
        });

        promise.success(function(){
            $scope.progress = 100;
            $scope.uploadState = $scope.STATUS.AWAITING;
            $scope.refresh();
        });

        promise.error(function(){
            $scope.uploadState = $scope.STATUS.ERROR;
        });
    };

    // loads the list of documents
    $scope.refresh = function(){
        var promise = repo.list();
        promise.success(function(data){
            $scope.documents = data;
        });
    };
    
    // load initial docs
    $scope.refresh();

    // remove socket handler when scope is destroyed
    $scope.$on('$destroy', function(){
        socket.off('document', onSocketDocument);
    });
}]);
