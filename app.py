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

    context = {
        "appversion": appversion,
        "footertext": footertext,
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
    if request.method == 'POST':
        newDataset = []
        form = request.form
        datasetSettings = {
            "numberOfProcesses": int(form.get("number-of-processes")),
            "minimumProcessDuration": int(form.get("minimum-process-duration")),
            "maximumProcessDuration": int(form.get("maximum-process-duration")),
            "randomizePriority": bool(form.get("randomize-priority")),
            "randomSeed": int(form.get("random-seed")),
            "numberOfPriorityLevels": int(form.get("number-of-priority-levels"))
        }
        newDataset.append(datasetSettings)
        if form.get("number-of-processes") != None:
            for x in range(datasetSettings.get('numberOfProcesses')):
                if datasetSettings['randomizePriority']:
                    priority = randint(1,datasetSettings['numberOfPriorityLevels'])
                else:
                    priority = 1
                newDataset.append({
                    "PID": x, 
                    "period-time": randint(datasetSettings['minimumProcessDuration'],datasetSettings['maximumProcessDuration']), 
                    "priority": priority
                    })
        print(newDataset)
        if newDataset != []:
            with open("./datasets/tmp.json", "w",) as f:
                json.dump(newDataset, f, indent=4)
        form = None
    
    context = {
        "appversion": appversion,
        "footertext": footertext,
    }
    return render_template("generator.html", context=context)


if __name__ == "__main__":
    app.run()
