from flask import Flask, request, jsonify, url_for, json
from connect4 import Connect4

app = Flask(__name__)

@app.route("/")
def index():
    return app.make_response(open('index.html').read())

@app.route('/here/now')
def difficulties():
    return app.send_static_file('difficulties.html')

@app.route('/process_move', methods=['POST'])
def move_response():

    request_json = request.get_json(force=True)
    board = request_json["board"]
    search_depth = int(request_json["search_depth"])
    con4 = Connect4(board, search_depth)
    result = con4.minimax()
    return jsonify(board=result[0], win=result[1])

@app.route('/check_for_p1_win', methods=['POST'])
def check_response():
    board = request.get_json(force=True)
    con4 = Connect4(board)
    p1_won = con4.check_for_p1_win()
    return jsonify(p1_won)




if __name__ == "__main__":
    app.run(debug=True)
