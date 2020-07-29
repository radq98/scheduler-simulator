from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    jsonify,
    redirect,
    url_for,
)
from datetime import datetime, timedelta
from random import randint
import json
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "5Q8wfQqmx67Ez0wondbxSeYXS8mE2gob"
app.config["DEBUG"] = True

# metadata
metadata = None
with open("meta.json", "r") as meta_file:
    metadata = json.load(meta_file)
appversion = metadata['appversion']
footertext = metadata['footertext']


@app.route("/", methods=["GET", "POST"])
def index():
    datasetsBase = os.listdir("./datasets/")
    context = {
        "appversion": appversion,
        "footertext": footertext,
        "datasetsBase": datasetsBase
    }
    return render_template("index.html", context=context)


@app.route("/results")
def results():
    context = {
        "appversion": appversion,
        "footertext": footertext,
    }
    return render_template("results.html", context=context)


@app.route("/generator", methods=["POST", "GET"])
def generator():
    #datasetsBase = [
    #    name
    #    for name in os.listdir("./datasets")
    #    if os.path.isdir(os.path.join("./datasets", name))
    #]
    
    if request.method == 'POST':
        newDataset = {"settings": None, "data": []}
        form = request.form
        datasetSettings = {
            "numberOfProcesses": int(form.get("number-of-processes")),
            "minimumProcessDuration": int(form.get("minimum-process-duration")),
            "maximumProcessDuration": int(form.get("maximum-process-duration")),
            "processDispersionFactor": int(form.get("process-dispersion-factor")),
            "randomizePriority": bool(form.get("randomize-priority")),
            #"randomSeed": int(form.get("random-seed")),
            "numberOfPriorityLevels": int(form.get("number-of-priority-levels"))
        }
        newDataset['settings'] = datasetSettings
        if form.get("number-of-processes") != None:
            lastArrive = 0
            arriveTime = 0
            for x in range(datasetSettings.get('numberOfProcesses')):
                if datasetSettings['randomizePriority']:
                    priority = randint(1,datasetSettings['numberOfPriorityLevels'])
                else:
                    priority = 1
                if lastArrive == 0:
                    lastArrive += 1
                else:
                    arriveTime = randint(lastArrive, lastArrive + int((datasetSettings['processDispersionFactor']/100) * datasetSettings['maximumProcessDuration']))
                    lastArrive = arriveTime
                newDataset['data'].append({
                    "PID": x, 
                    "arrive-time": arriveTime,
                    "period-time": randint(datasetSettings['minimumProcessDuration'],datasetSettings['maximumProcessDuration']), 
                    "priority": priority
                    })
        uniqueDatasetId= randint(10000,99999)
        datenow = datetime.now().date()
        if newDataset != []:
            with open("./datasets/dataset-"+str(datenow)+"-"+str(uniqueDatasetId)+".json", "w",) as f:
                json.dump(newDataset, f, indent=4)
        form = None
    datasetsBase = os.listdir("./datasets/")
    context = {
        "appversion": appversion,
        "footertext": footertext,
        "datasetsBase": datasetsBase
    }
    return render_template("generator.html", context=context)


if __name__ == "__main__":
    app.run()
