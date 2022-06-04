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
    try:
        run_cmd(f"tkn pipeline start {config['pipeline']['train']}")

        return jsonify("Training successfull")

    except Exception as e:
        raise e


@cross_origin()
@app.route("/predict", methods=["GET"])
def prediction_route():
    try:
        run_cmd(f"tkn pipeline start {config['pipeline']['pred']}")

        return jsonify("Prediction successfull")

    except Exception as e:
        raise e


if __name__ == "__main__":
    app.run(host=config["app"]["host"], port=config["app"]["port"])
