from flask import Flask, send_file
from flask import Response
from flask import request
from flask import jsonify

from io import BytesIO
from drugClass import drugObj

app = Flask(__name__)


@app.route('/test', methods=['POST'])
def test():
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
        drugobj = drugObj(drug, weeks, source, predictBool)
        drugobj.availableGraphs[chartType]['function'](weeks, predictBool)
        fig = drugobj.availableGraphs[chartType]['figName'].fig
        img = BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype='image/png')
    else:
        return "Unsupported mediatype"


if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=80)
