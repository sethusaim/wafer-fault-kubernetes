from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from pipelines.prediction_pipeline import Pred_Pipeline
from pipelines.train_pipeline import Train_Pipeline
from utils.main_utils import Main_Utils
from utils.read_params import read_params

app = FastAPI()

config = read_params()

templates = Jinja2Templates(config["templates"]["dir"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        config["templates"]["index"], {"request": request}
    )
    

@app.get("/train")
def trainRouteClient():
    try:
        pipeline = Train_Pipeline()

        pipeline.run_train_pipeline(config["pipeline_path"]["train"])

        return Response("Training successfull!!")

    except Exception as e:
        return Response(f"Error Occurred : {e}")


@app.get("/predict")
def predictRouteClient():
    try:
        pipeline = Pred_Pipeline()

        pipeline.run_pred_pipeline(config["pipeline_path"]["pred"])

        return Response("Prediction Successfull")

    except Exception as e:
        return Response(f"Error Occurred : {e}")


if __name__ == "__main__":
    try:
        app_run(app, host=config["app"]["host"], port=config["app"]["port"])

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
