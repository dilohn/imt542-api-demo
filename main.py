YOUR_TOKEN = "YOUR_TOKEN"


import threading
import time
import json

from flask import Flask, request, jsonify
from pyngrok import ngrok
import requests

app = Flask(__name__)


def read_json_file(filename):
    with open(filename, "r") as f:
        return json.load(f)


# Test dataset or your equivalent sbir-search-results.json in the same folder
my_data = read_json_file("sbir-search-results.json")


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"


@app.route("/hello/name/<username>", methods=["GET"])
def hello_user(username):
    return f"hello {username}"


@app.route("/info", methods=["GET"])
def info():
    return (
        "Hello, I am your API.\n"
        "You can call:\n"
        "  GET  /hello/name/<username>\n"
        "  GET  /sbir/state/<state>\n"
        "  POST /sbir/state  (JSON body: {'state': 'CA'})\n"
    )


@app.route("/sbir/state/<state>", methods=["GET"])
def sbir_by_state(state):
    for entry in my_data:
        if entry.get("State") == state:
            return entry.get("Award_Title", "No Title")
    return "none", 404


@app.route("/sbir/state", methods=["POST"])
def sbir_by_state_post():
    payload = request.get_json() or {}
    state = payload.get("state")
    for entry in my_data:
        if entry.get("State") == state:
            return jsonify({"Award_Title": entry.get("Award_Title")})
    return jsonify({"error": "state not found"}), 404


def start_flask():
    # Running with debug=False so it doesn't spawn extra threads on Windows
    app.run(port=5000, debug=False)


if __name__ == "__main__":
    # Start Flask in a background thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    time.sleep(1)

    # ngrok tunnel
    ngrok.set_auth_token(YOUR_TOKEN)
    public_url = ngrok.connect(5000).public_url
    print(f'ngrok tunnel "{public_url}" -> "http://127.0.0.1:5000"')

    # use requests to call the root ("/") endpoint over the tunnel
    resp = requests.get(public_url)
    print("Response from API:", resp.text)  # should print "Hello, World!"

    # Keep the script alive until you want out
    input("\nPress Enter to shut down\n")
