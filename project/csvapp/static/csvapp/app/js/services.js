'use strict';


angular.module('app.services', [])
.factory('csvSocket', function(){
    var socket = io.connect('/csv');
    return {
        on: function(event, listener){
            socket.on(event, listener);
        },

        off: function(event, listener){
            socket.removeListener(event, listener);
        }
    };
})

.factory('documentRepository', ['$http', '$upload', 'documentEndpoint', function($http, $upload, endpoint){
    return {
        list: function(){
            var promise = $http.get(endpoint);
            return promise;
        },

        create: function(file){
            var promise = $upload.upload({
                url: endpoint,
                file: file
            });

            return promise;
        },

        get: function(id){
            var promise = $http.get(endpoint + id + '/');
            return promise;
        }
    };
}])

.factory('sortedDocumentRepository', ['$http', 'sortedDocumentEndpoint', function($http, endpoint){
    return {
        create: function(doc, columnName, ascending){
            var promise = $http.post(endpoint, {
                doc: doc,
                column: columnName,
                ascending: ascending
            });

            return promise;
        },

        get: function(id){
            var promise = $http.get(endpoint + id + '/');
            return promise;
        }
    };
}])