from subprocess import run as run_cmd

from flask import Flask, Response, jsonify, render_template
from flask_cors import CORS, cross_origin

from src.constant.application import APP_HOST, APP_PORT, INDEX_HTML
from src.constant.pipeline import PRED_PIPELINE, TRAIN_PIPELINE

app = Flask(__name__)

CORS(app)


@cross_origin()
@app.route("/", methods=["GET"])
def home():
    return render_template(INDEX_HTML)


@cross_origin()
@app.route("/train", methods=["GET"])
def train_route():
    try:
        run_cmd(["tkn", "pipeline", "start", TRAIN_PIPELINE])

        return jsonify("Training successfull")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@cross_origin()
@app.route("/predict", methods=["GET"])
def prediction_route():
    try:
        run_cmd(["tkn", "pipeline", "start", PRED_PIPELINE])

        return jsonify("Prediction successfull")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
