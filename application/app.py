from subprocess import run as run_cmd

from flask import Flask, Response, jsonify
from flask_cors import CORS, cross_origin

from src.constant.application import APP_HOST, APP_PORT
from src.constant.pipeline import TRAIN_PIPELINE

app = Flask(__name__)

CORS(app)

@cross_origin()
@app.route("/train", methods=["GET"])
def train_route():
    try:
        run_cmd(["tkn", "pipeline", "start", TRAIN_PIPELINE])

        return jsonify("Training successfull")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
