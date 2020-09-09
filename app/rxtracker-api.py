from flask import Flask, send_file, Response, request, jsonify

from io import BytesIO
import base64
import pandas as pd
import matplotlib.pyplot as plt
import mpld3

from drugClass import drugObj
import modelClass

app = Flask(__name__)


@app.route("/healthCheck")
def healthCheck():
    return Response(status=200)


@app.route("/chart", methods=["POST"])
def chart():
    if request.headers["Content-Type"] == "application/json":
        drug = request.get_json()["drug"]
        chartType = request.get_json()["chartType"]
        weeks = request.get_json()["weeks"]
        predictBool = request.get_json()["predictBool"]
        source = request.get_json()["source"]
        weeksToTrainOn = request.get_json()["weeksToTrainOn"]
        figW = request.get_json()["figWidth"]
        figH = request.get_json()["figHeight"]

        drugobj = drugObj(drug, weeks, source, predictBool,
                          weeksToTrainOn, figW, figH)
        availableGraphs = drugobj.generateAvailableGraphsDict()
        availableGraphs[chartType]["function"](weeks, predictBool)
        availableGraphs = drugobj.generateAvailableGraphsDict()

        fig = availableGraphs[chartType]["figName"].fig
        img = BytesIO()
        fig.savefig(img)
        img.seek(0)
        img_b64 = base64.b64encode(img.read())
        return Response(img_b64, status=200, mimetype="application/json")
    else:
        return "Unsupported mediatype"


@app.route("/interactive", methods=["POST"])
def interactive():
    if request.headers["Content-Type"] == "application/json":
        drug = request.get_json()["drug"]
        chartType = request.get_json()["chartType"]
        weeks = request.get_json()["weeks"]
        predictBool = request.get_json()["predictBool"]
        source = request.get_json()["source"]
        weeksToPredict = request.get_json()["weeksToPredict"]
        weeksToTrainOn = request.get_json()["weeksToTrainOn"]

        figW = request.get_json()["figWidth"]
        figH = request.get_json()["figHeight"]

        drugobj = drugObj(drug, weeks, source, predictBool,
                          weeksToTrainOn, figW, figH, weeksToPredict)
        availableGraphs = drugobj.generateAvailableGraphsDict()
        availableGraphs[chartType]["function"](weeks, predictBool)
        availableGraphs = drugobj.generateAvailableGraphsDict()

        fig = availableGraphs[chartType]["figName"].fig
        html_str = mpld3.fig_to_html(fig)
        return Response(html_str, status=200)
    else:
        return "Unsupported mediatype"


@app.route("/prediction", methods=["POST"])
def prediction():
    if request.headers["Content-Type"] == "application/json":
        drug = request.get_json()["drug"]
        weeks = request.get_json()["weeks"]
        source = request.get_json()["source"]
        predictBool = request.get_json()["predictBool"]
        weeksToTrainOn = request.get_json()["weeksToTrainOn"]
        drugobj = drugObj(drug, weeks, source, predictBool, weeksToTrainOn)

        target = request.get_json()["target"]
        weeksToPredict = request.get_json()["weeksToPredict"]
        predictionDf = modelClass.modelObj(
            drugobj.masterDf, drugobj.weeksToTrainOn, target, weeksToPredict
        ).predictionDf
        return predictionDf.to_json(orient="records")
    else:
        return "Unsupported mediatype"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
