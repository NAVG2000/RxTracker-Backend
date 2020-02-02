from flask import Flask, send_file, Response, request, jsonify

from io import BytesIO
import pandas as pd

from drugClass import drugObj
import modelClass

app = Flask(__name__)


@app.route('/test', methods=['POST'])
def test():
    resp = Response("working", status=200, mimetype='application/json')
    return resp

@app.route('/testget', methods=['GET'])
def testget():
    resp = Response("working", status=200, mimetype='application/json')
    return resp


@app.route('/chart', methods=['POST'])
def chart():
    if request.headers['Content-Type'] == 'application/json':
        drug = request.get_json()['drug']
        chartType = request.get_json()['chartType']
        weeks = request.get_json()['weeks']
        predictBool = request.get_json()['predictBool']
        source = request.get_json()['source']
        weeksToTrainOn = request.get_json()['weeksToTrainOn']

        drugobj = drugObj(drug, weeks, source, predictBool, weeksToTrainOn)
        availableGraphs = drugobj.generateAvailableGraphsDict()
        availableGraphs[chartType]['function'](weeks, predictBool)
        availableGraphs = drugobj.generateAvailableGraphsDict()

        fig = availableGraphs[chartType]['figName'].fig
        img = BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype='image/png')
    else:
        return "Unsupported mediatype"


@app.route('/prediction', methods=['POST'])
def prediction():
    if request.headers['Content-Type'] == 'application/json':
        drug = request.get_json()['drug']
        weeks = request.get_json()['weeks']
        source = request.get_json()['source']
        predictBool = request.get_json()['predictBool']
        weeksToTrainOn = request.get_json()['weeksToTrainOn']
        drugobj = drugObj(drug, weeks, source, predictBool, weeksToTrainOn)

        target = request.get_json()['target']
        weeksToPredict = request.get_json()['weeksToPredict']
        predictionDf = modelClass.modelObj(
            drugobj.masterDf, drugobj.weeksToTrainOn, target, weeksToPredict).predictionDf
        return predictionDf.to_json(orient="records")
    else:
        return "Unsupported mediatype"


if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8000)
