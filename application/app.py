from subprocess import run as run_cmd

from flask import Flask, jsonify, render_template
from flask_cors import CORS, cross_origin

from utils.read_params import read_params

app = Flask(__name__)

CORS(app)

config = read_params()


@cross_origin()
@app.route("/", methods=["GET"])
def home():
    return render_template(config["templates"]["index"])


@cross_origin()
@app.route("/train", methods=["GET"])
def train_route():
    run_cmd(f"tkn pipeline start {config['pipeline']['train']}")

    return jsonify("Training successfull")


@cross_origin()
@app.route("/predict", methods=["GET"])
def prediction_route():
    run_cmd(f"tkn pipeline start {config['pipeline']['pred']}")

    return jsonify("Prediction successfull")


if __name__ == "__main__":
    app.run(host=config["app"]["host"], port=config["app"]["port"])
