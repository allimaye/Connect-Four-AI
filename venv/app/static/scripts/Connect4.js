

(function () {

    var app = angular.module('Connect Four', ['ngMaterial', 'ngMessages', 'ngSanitize']);



    app.controller('InputController', function ($scope, $mdDialog, $interval, $filter, $http,
        $timeout, $sanitize, $interval, $window) {

        



        //$scope.pageHeight = $window.innerHeight;
        //$scope.pageWidth = $window.innerWidth;
        
        //$scope.buttonStyle = {
        //    'margin-left': $scope.pageWidth*0.004+'px', 
        //    'margin-right': $scope.pageWidth*0.004+'px',
        //    'width': $scope.pageHeight*0.085+'px', 
        //    'height': $scope.pageHeight * 0.085 + 'px',
        //    'line-height': '0px',
        //    'min-height': '0px'
        //};
        //$scope.iconStyle = {
        //    'width': $scope.pageHeight * 0.0425 + 'px !important',
        //    'height': $scope.pageHeight * 0.0425 + 'px !important'
        //};
        //$scope.slotStyle = {
        //    'width': $scope.pageHeight * 0.095 + 'px',
        //    'height': $scope.pageHeight * 0.095 + 'px',
        //    'border-radius': '0 0 0 0'
        //};
        //$scope.titleStyle = {
        //    'height': $scope.pageHeight * 0.07 + 'px',
        //};

        $scope.buttonStyle = {
            'margin-left': '0px', 
            'margin-right': '0px',
            'width': '0px',
            'height': '0px',
            'line-height': '0px',
            'min-height': '0px'
        };
        $scope.iconStyle = {
            'width': '0px',
            'height': '0px'
        };
        $scope.slotStyle = {
            'width': '0px',
            'height': '0px',
            'border-radius': '0 0 0 0'
        };
        $scope.titleStyle = {
            'height': '0px',
        };



        $scope.$watch(function () { return $window.innerWidth; },
            function (value) {
                console.log(value);

                var padding_h = parseInt($("#content").css("padding-top")) + parseInt($("#content").css("padding-bottom"));
                var img_height = parseInt(($window.innerHeight - padding_h) / 9);
                var padding_w = parseInt($("#content").css("padding-right")) + parseInt($("#content").css("padding-left"));
                var img_width = parseInt(($("#card").width() - padding_w) / 7);
                var img_len = Math.min(img_height, img_width);
                $scope.titleStyle['height'] = img_len * 1.0 + 'px';
                $scope.slotStyle.width = img_len + 'px';
                $scope.slotStyle.height = img_len + 'px';
                $scope.buttonStyle['margin-left'] = img_len * 0.1 + 'px';
                $scope.buttonStyle['margin-right'] = img_len * 0.1 + 'px';
                $scope.buttonStyle['width'] = img_len * 0.8 + 'px';
                $scope.buttonStyle['height'] = img_len * 0.8 + 'px';
                $scope.iconStyle['width'] = img_len * 0.8 * 0.5 + 'px';
                $scope.iconStyle['height'] = img_len * 0.8 * 0.5 + 'px';


                
          },
          true
        );

        angular.element($window).bind('resize', function () {
            $scope.$apply();
        });











        //$scope.card_height = $("#card").height();
        //$scope.card_width = $("#card").width();

        //$scope.buttonStyle = {
        //    'margin-left': $scope.card_width * 0.004 + 'px',
        //    'margin-right': $scope.card_width * 0.004 + 'px',
        //    'width': $scope.card_width * 0.085 + 'px',
        //    'height': $scope.card_width * 0.085 + 'px',
        //    'line-height': '0px'
        //};
        //$scope.iconStyle = {
        //    'width': $scope.card_width * 0.0425 + 'px',
        //    'height': $scope.card_width * 0.0425 + 'px'
        //};
        
        //$scope.content_padding = parseInt($("#content").css("padding-right")) + parseInt($("#content").css("padding-left"));
        //$scope.img_width = parseInt(($scope.card_width - $scope.content_padding) / 7);

        //$scope.slotStyle = {
        //    //'width': $scope.card_width * 0.095 + 'px',
        //    //'height': $scope.card_width * 0.095 + 'px',
        //    'width': $scope.img_width + 'px',
        //    'border-radius': '0 0 0 0'
        //};


        $scope.columns = [];
        $scope.rows = [];
        $scope.p1_won = false;
        $scope.user_msg = "";

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
                $scope.user_msg = "The computer is thinking...";
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

            $scope.user_msg = "";
            $scope.cpu_thinking = false;
            
        }

        $scope.get_CPU_response = function () {

            var sent_data = {
                "board": $scope.board,
                "search_depth": $scope.search_depth
            };

            $http.post('/process_move', JSON.stringify(sent_data))
            .then(function successCallback(response) {
                //Error on server side
                if (response.data.board.length == 0) {
                    location.reload();
                }

                $scope.board = response.data.board;
                var cpu_win = response.data.win;
                if (cpu_win) {
                    show_winner(2, response.data.streak);
                    var promise = $timeout(function () { $scope.on_game_end(2) }, 4400);
                }
                else {
                    //check the board to see if it is completely full. In this case, it's a draw.
                    var draw = true;
                    for (var row = 0; row < 6; row++) {
                        for (var col = 0; col < 7; col++) {
                            if ($scope.board[row][col] == 0) {
                                draw = false;
                                break;
                            }
                        }
                    }

                    if (draw) {
                        var promise = $timeout(function () { $scope.on_game_end(null) }, 100);
                        $scope.user_msg = "";
                    }
                    else {
                        $scope.user_msg = "The computer has made its' move!";
                    }
                }
                $scope.cpu_thinking = false;
                
            }, function errorCallback(response) {
                console.log(response.data);
                console.log(response.status);
            });
        };

        $scope.check_for_p1_win = function () {
            $http.post('/check_for_p1_win', JSON.stringify($scope.board))
            .then(function successCallback(response) {
                var p1_won = response.data.win;
                if (p1_won) {
                    show_winner(1, response.data.streak);
                    var promise = $timeout(function () { $scope.on_game_end(1) }, 4400);
                }
                else {
                    $scope.get_CPU_response();
                }
            }, function errorCallback(response) {
                console.log(response.data);
                console.log(response.status);
            });
        };

        $scope.on_game_end = function (winner) {
            var title = message = label = "";
            if (winner == 2) {
                title = "Computer Wins!";
                message = "The computer has won. The board has been reset.";
                label = "Computer Won";
            }
            else if(winner == 1) {
                title = "You Win!";
                message = "You have won. The board has been reset.";
                label = "You Won";
            }
            else {
                title = "It's a Draw!";
                message = "This game is a draw. The board has been reset.";
                label = "It's a Draw!";
            }

            var win_dialog = $mdDialog.alert()
                .clickOutsideToClose(true)
                .title(title)
                .textContent(message)
                .ariaLabel(label)
                .ok('Got it!');

            $mdDialog.show(win_dialog).then(function(result) {
                $scope.init_board();
            });

            
        };

        

        $scope.flash_pieces = function (streak, current_player) {

            for (var j = 0; j < streak.length; j++) {
                var coordinates = streak[j]
                var row = coordinates[0];
                var col = coordinates[1];
                $scope.board[row][col] = current_player;
            };

        };

        function show_winner(player, streak) {
            for (var x = 0; x < 14; x++) {
                flash_winner(x, player, streak);
            }
        }

        function flash_winner(x, player, streak) {
            var current_player = x % 2 ? 0 : player;
            $timeout(function () { $scope.flash_pieces(streak, current_player) }, x * 300);
        }


        $scope.init_board();


    });

})();

