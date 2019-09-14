from flask import Flask, send_file
from flask import Response
from flask import request
from flask import jsonify

from io import BytesIO
from drugClass import drugObj

app = Flask(__name__)


def generateAvailableGraphsDict():
    availableGraphs = {
        "graph_normalizedTRxAndAllMAs": {'function': drugobj.graph_normalizedTRxAndAllMAs, 'figName': drugobj.normalizedTRxAndAllMAsChart},
        "graph_normalizedTRx": {'function': drugobj.graph_normalizedTRx, 'figName': drugobj.normalizedTRxChart},
        "graph_fourWeekMATRx": {'function': drugobj.graph_fourWeekMATRx, 'figName': drugobj.fourWeekMATRxChart},
        "graph_eightWeekMATRx": {'function': drugobj.graph_eightWeekMATRx, 'figName': drugobj.eightWeekMATRxChart},
        "graph_thirteenWeekMATRx": {'function': drugobj.graph_thirteenWeekMATRx, 'figName': drugobj.thirteenWeekMATRxChart},
        "graph_normalizedTRxLog": {'function': drugobj.graph_normalizedTRxLog, 'figName': drugobj.normalizedTRxLogChart},
        "graph_normalizedNRx": {'function': drugobj.graph_normalizedNRx, 'figName': drugobj.normalizedNRxChart},
        "graph_fourWeekMANRx": {'function': drugobj.graph_fourWeekMANRx, 'figName': drugobj.fourWeekMANRxChart},
        "graph_eightWeekMANRx": {'function': drugobj.graph_eightWeekMANRx, 'figName': drugobj.eightWeekMANRxChart},
        "graph_thirteenWeekMANRx": {'function': drugobj.graph_thirteenWeekMANRx, 'figName': drugobj.thirteenWeekMANRxChart},
        "graph_normalizedNRxLog": {'function': drugobj.graph_normalizedNRxLog, 'figName': drugobj.normalizedNRxLogChart},
        "graph_normalizedRRx": {'function': drugobj.graph_normalizedRRx, 'figName': drugobj.normalizedRRxChart},
        "graph_fourWeekMARRx": {'function': drugobj.graph_fourWeekMARRx, 'figName': drugobj.fourWeekMARRxChart},
        "graph_eightWeekMARRx": {'function': drugobj.graph_eightWeekMARRx, 'figName': drugobj.eightWeekMARRxChart},
        "graph_thirteenWeekMARRx": {'function': drugobj.graph_thirteenWeekMARRx, 'figName': drugobj.thirteenWeekMARRxChart},
        "graph_normalizedRRxLog": {'function': drugobj.graph_normalizedRRxLog, 'figName': drugobj.normalizedRRxLogChart},
        "graph_trxWowGrowth": {'function': drugobj.graph_trxWowGrowth, 'figName': drugobj.trxWowGrowthChart},
        "graph_fourWeekMATRxWoWGrowth": {'function': drugobj.graph_fourWeekMATRxWoWGrowth, 'figName': drugobj.fourWeekMATRxWoWGrowthChart},
        "graph_eightWeekMATRxWoWGrowth": {'function': drugobj.graph_eightWeekMATRxWoWGrowth, 'figName': drugobj.eightWeekMATRxWoWGrowthChart},
        "graph_thirteenWeekMATRxWoWGrowth": {'function': drugobj.graph_thirteenWeekMATRxWoWGrowth, 'figName': drugobj.thirteenWeekMATRxWoWGrowthChart},
        "graph_nrxWowGrowth": {'function': drugobj.graph_nrxWowGrowth, 'figName': drugobj.nrxWowGrowthChart},
        "graph_fourWeekMANRxWoWGrowth": {'function': drugobj.graph_fourWeekMANRxWoWGrowth, 'figName': drugobj.fourWeekMANRxWoWGrowthChart},
        "graph_eightWeekMANRxWoWGrowth": {'function': drugobj.graph_eightWeekMANRxWoWGrowth, 'figName': drugobj.eightWeekMANRxWoWGrowthChart},
        "graph_thirteenWeekMANRxWoWGrowth": {'function': drugobj.graph_thirteenWeekMANRxWoWGrowth, 'figName': drugobj.thirteenWeekMANRxWoWGrowthChart},
        "graph_rrxWowGrowth": {'function': drugobj.graph_rrxWowGrowth, 'figName': drugobj.rrxWowGrowthChart},
        "graph_fourWeekMARRxWoWGrowth": {'function': drugobj.graph_fourWeekMARRxWoWGrowth, 'figName': drugobj.fourWeekMARRxWoWGrowthChart},
        "graph_eightWeekMARRxWoWGrowth": {'function': drugobj.graph_eightWeekMARRxWoWGrowth, 'figName': drugobj.eightWeekMARRxWoWGrowthChart},
        "graph_thirteenWeekMARRxWoWGrowth": {'function': drugobj.graph_thirteenWeekMARRxWoWGrowth, 'figName': drugobj.thirteenWeekMARRxWoWGrowthChart},
        "graphNormalizedAllRx": {'function': drugobj.graphNormalizedAllRx, 'figName': drugobj.normalizedAllRxChart}
    }
    return availableGraphs


@app.route('/test', methods=['POST'])
def test():
    resp = Response("working", status=200, mimetype='application/json')
    return resp


@app.route('/chart', methods=['POST'])
def testChart():
    if request.headers['Content-Type'] == 'application/json':
        drug = request.get_json()['drug']
        chartType = request.get_json()['chartType']
        weeks = request.get_json()['weeks']
        predictBool = request.get_json()['predictBool']
        source = request.get_json()['source']
        drugobj = drugObj(drug, weeks, source, predictBool)
        availableGraphs = generateAvailableGraphsDict()
        availableGraphs[chartType]['function'](weeks, predictBool)
        fig = availableGraphs[chartType]['figName'].fig
        img = BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype='image/png')
    else:
        return "Unsupported mediatype"


if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=80)
