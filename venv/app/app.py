from flask import Flask, request, jsonify, url_for, json
from connect4 import Connect4

app = Flask(__name__)

@app.route("/")
def index():
    return app.make_response(open('index.html').read())

@app.route('/process_move', methods=['POST'])
def move_response():
    try:
        request_json = request.get_json(force=True)
        board = request_json["board"]
        search_depth = int(request_json["search_depth"])
        con4 = Connect4(board, search_depth)
        result = con4.minimax()
        return jsonify(board=result[0], win=result[1], streak=result[2])
    except:
        # indicate to client that an error has occured by sending input board back
        return jsonify(board=[], win=False, streak=[])


@app.route('/check_for_p1_win', methods=['POST'])
def check_response():
    try:
        board = request.get_json(force=True)
        con4 = Connect4(board)
        result = con4.check_for_p1_win()
        if(result[0]):
            return jsonify(win=result[0], streak=result[1])
        else:
            return jsonify(win=result[0])
    except:
        return jsonify(win=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
