

(function () {

    var app = angular.module('Connect Four', ['ngMaterial', 'ngMessages', 'ngSanitize']);

    app.controller('InputController', function ($scope, $mdDialog, $interval, $filter, $http, $timeout, $sanitize) {
        

        $scope.pageHeight = window.outerHeight

        $scope.card_width = $("#card").width();
        $scope.content_padding = parseInt($("#content").css("padding-right")) + parseInt($("#content").css("padding-left"));
        $scope.img_width = parseInt(($scope.card_width - $scope.content_padding) / 7)

        $boardrow_width = $("#boardrow1").width();

        $scope.columns = [];
        $scope.rows = [];
        $scope.p1_won = false;
        $scope.user_msg = $scope.cpu_thinking ? "The computer is thinking..." : "The computer has made its' move!";

        //each difficulty corresponds with a search depth. The JSON has key = difficulty, value = search depth
        $scope.difficulty_mappings = {
            "Beginner": 2,
            "Intermediate": 3,
            "Expert": 5
        };

        $scope.difficulties = Object.keys($scope.difficulty_mappings) 
        $scope.search_depth = 3;
        $scope.cpu_thinking = false;
        

        $scope.addPiece = function (col) {

            var piece_added = false
            for (var i = 5; i >= 0; i--) {
                if ($scope.board[i][col] == 0) {
                    $scope.board[i][col] = 1;
                    piece_added = true;
                    break;
                }
            }

            if (piece_added) {
                // see if the human player (p1) won.
                $scope.cpu_thinking = true;
                $scope.check_for_p1_win();
            }
            
        };

        $scope.init_board = function () {
            $scope.board = []
            for (var rowNum = 0; rowNum < 6; rowNum++) {
                var row = [];
                for (var colNum = 0; colNum < 7; colNum++) {
                    row.push(0);
                }
                $scope.board.push(row)
            }
            $scope.cpu_win = false;

            $mdDialog.show({
                scope: $scope,        // use parent scope in template
                preserveScope: true,
                templateUrl: 'static/views/difficulty.html',
                controller: function DialogController($scope, $mdDialog) {

                    $scope.difficulty_mappings = {
                        "Beginner": 2,
                        "Intermediate": 3,
                        "Expert": 5
                    };

                    $scope.difficulties = Object.keys($scope.difficulty_mappings)
                    $scope.search_depth = 3;

                    $scope.closeDialog = function () {
                        $mdDialog.hide();
                    };
                }
            });

        }

        $scope.get_CPU_response = function () {

            //var sent_data = JSON.stringify($scope.board);
            var sent_data = {
                "board": $scope.board,
                "search_depth": $scope.search_depth
            };

            $http.post('/process_move', JSON.stringify(sent_data))
            .success(function (data, status, headers, config) {
                $scope.board = data.board;
                var cpu_win = data.win;
                if (cpu_win) {
                    var promise = $timeout(function () { $scope.on_player_win(true) }, 3000);
                }      
            })
            .error(function (data, status, header, config) {
                console.log(data)
                console.log(status)
            });

        };

        $scope.check_for_p1_win = function () {
            $http.post('/check_for_p1_win', JSON.stringify($scope.board))
           .success(function (data, status, headers, config) {
               var p1_won = data;
               if (p1_won) {
                   var promise = $timeout(function () { $scope.on_player_win(false) }, 2000);
               }
               else {
                   $scope.get_CPU_response();
               }
               $scope.cpu_thinking = false;
           })
           .error(function (data, status, header, config) {
               console.log(data)
               console.log(status)
           });
        }


        $scope.on_player_win = function (p2) {
            var title = message = label = "";
            if (p2) {
                title = "Computer Wins!";
                message = "The computer has won. The board has been reset.";
                label = "Computer Won";
            }
            else {
                title = "You Win!";
                message = "You have won. The board has been reset.";
                label = "You Won";
            }

            $mdDialog.show(
                $mdDialog.alert()
                .clickOutsideToClose(true)
                .title(title)
                .textContent(message)
                .ariaLabel(label)
                .ok('Got it!')
            );

            $scope.init_board();
        };

        $scope.init_board();



        function sleep(seconds) {
            var e = new Date().getTime() + (seconds * 1000);
            while (new Date().getTime() <= e) { }
        }



    });

})();

