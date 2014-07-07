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
        if ($scope.uploadState !== $scope.STATUS.WAITING) return;
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
}])

.controller('DocumentCtrl', ['$scope', '$routeParams', 'csvSocket', 'documentRepository', 'sortedDocumentRepository', 'MEDIA_URL',
        function($scope, $routeParams, socket, docRepo, sortRepo, MEDIA_URL) {

    $scope.MEDIA_URL = MEDIA_URL;
    $scope.STATUS = {
        WAITING: 0,
        DISABLED: 1,
        AWAITING: 2, // awaiting socketio message
        READY: 3,
        ERROR: 4
    };

    $scope.createState = $scope.STATUS.WAITING;

    // spits out duplicate metadata
    var onSocketSortedDocument = function(data){
        var promise = sortRepo.get(data.id);
        promise.success(function(data){
            $scope.createState = $scope.STATUS.READY;
            $scope.newDoc = data;
            $scope.$apply();
            $scope.refresh();
        });
        promise.error(function(){
            $scope.createState = $scope.STATUS.ERROR;
        });
    };
    socket.on('sorteddocument', onSocketSortedDocument);

    // handle form submit
    $scope.create = function(form){
        if ($scope.createState !== $scope.STATUS.WAITING) return;
        $scope.createState = $scope.STATUS.WAITING;

        var promise = sortRepo.create(parseInt($routeParams.id), $scope.columnName, $scope.columnAscending === 'true');

        promise.success(function(){
            $scope.createState = $scope.STATUS.AWAITING;
        });

        promise.error(function(){
            $scope.createState = $scope.STATUS.ERROR;
        });
    };

    // loads the list of sorted documents
    $scope.refresh = function(){
        var promise = docRepo.get(parseInt($routeParams.id));
        promise.success(function(data){
            $scope.doc = data;
            $scope.sortedDocuments = data.sorted_documents;
        });
    };

    // load initial docs
    $scope.refresh();

    // remove socket handler when scope is destroyed
    $scope.$on('$destroy', function(){
        socket.off('sorteddocument', onSocketSortedDocument);
    });
}]);

