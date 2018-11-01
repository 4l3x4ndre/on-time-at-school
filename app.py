from flask import Flask, render_template, request, jsonify
from stif import stif, ledSTIF, msgSTIF
from vianavigo import vianavigo, ledVianavigo, messagesVianavigo


app = Flask(__name__)


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


@app.route("/")
def api():

    stif()
    vianavigo()

    ledFinale = {
        "rouge": max(ledSTIF["rouge"], ledVianavigo["rouge"]),
        "orange": max(ledSTIF["orange"], ledVianavigo["orange"]),
        "vert": max(ledSTIF["vert"], ledVianavigo["vert"]),
    }
    if request_wants_json():
        return jsonify(ledFinale)
    else:
        return render_template("api.html", ledSTIF = ledSTIF, messagesSTIF = list(map(lambda x: "STIF: "+x, msgSTIF)),
                               ledVianavigo = ledVianavigo, messagesVianavigo = list(map(lambda x: "Vianavigo: "+x,
                                                                                         messagesVianavigo)),
                               ledFinale = ledFinale)

if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug=True, use_debugger=True)
