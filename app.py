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

# scheduler class

#class Scheduler:
#  def __init__(self, dataset, age):
#    self.dataset = dataset
#    self.age = age

#  def myfunc(self):
#    print("Hello my name is " + self.name)

#p1 = Person("John", 36)
#p1.myfunc()

@app.route('/_get_results')
def get_results():
    simulationSettings = {
        "algorithm": request.args.get('algorithm', None, type=str),
        "dataset": request.args.get('dataset', None, type=str),
        "visualization": request.args.get('visualization', None, type=str),
        "rrInterval": request.args.get('rrInterval', None, type=str),
        "agingPriorities": request.args.get('agingPriorities', None, type=str),
        "ppAgingInterval": request.args.get('ppAgingInterval', None, type=str)
    }
    dataset = None
    with open("./datasets/" + simulationSettings['dataset'], "r") as f:
        dataset = json.load(f)
    
    steps = []
    values = []

    #scheduling FCFS
    def newStep(time, eventType, PID):
        return {"time": time, "eventType": eventType, "PID": PID}
    
    def newValue(currentTime, toProcessCount, processedCount, queueList, processingList, processedList):
        return {"currentTime": currentTime, "toProcessCount": toProcessCount, "processedCount": processedCount, "queueList": queueList, "processingList": processingList, "processedList": processedList}
    currentTime = 0
    toProcessCount = dataset['settings']['numberOfProcesses']
    processedCount = 0
    queueList = dataset['data']
    #adding necessary parameters to process objects
    for x in queueList:
        x["waitingTime"] = 0
    
    processingList = []
    processedList = []
    while toProcessCount > 0:
        values.append(newValue(currentTime, toProcessCount, processedCount, queueList.copy(), processingList.copy(), processedList.copy()))
        for x in queueList:
            if x['arrive-time'] == currentTime:
                processingList.append(x.copy())
                queueList.remove(x)
                steps.append(newStep(currentTime, "arrive", str(processingList[-1]['PID'])))
        if len(processingList) > 0:
            if len(processingList) > 1:
                for x in processingList:
                    if x != processingList[0]:
                        x['waitingTime'] += 1
            steps.append(newStep(currentTime, "processing", str(processingList[0]['PID'])))
            processingList[0]['period-time'] -= 1
            if processingList[0]['period-time'] == 0:
                processedList.append(processingList[0].copy())
                steps.append(newStep(currentTime, "finished", str(processingList[0]['PID'])))
                processingList.pop(0)
                toProcessCount -= 1
                processedCount += 1
            if toProcessCount>0:
                currentTime += 1
        else:
            steps.append(newStep(currentTime, "no-task", None))
            currentTime += 1
    steps.append(newStep(currentTime, "simulation-finished", None))
    values.append(newValue("finished", toProcessCount, processedCount, queueList.copy(), processingList.copy(), processedList.copy()))
    results = {
        "settings": simulationSettings,
        "steps": steps,
        "values": values.copy()
    }
    print(results)

    return jsonify(results)


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
    # datasetsBase = [
    #    name
    #    for name in os.listdir("./datasets")
    #    if os.path.isdir(os.path.join("./datasets", name))
    # ]

    if request.method == 'POST':
        newDataset = {"settings": None, "data": []}
        form = request.form
        datasetSettings = {
            "numberOfProcesses": int(form.get("number-of-processes")),
            "minimumProcessDuration": int(form.get("minimum-process-duration")),
            "maximumProcessDuration": int(form.get("maximum-process-duration")),
            "processDispersionFactor": int(form.get("process-dispersion-factor")),
            "randomizePriority": bool(form.get("randomize-priority")),
            # "randomSeed": int(form.get("random-seed")),
            "numberOfPriorityLevels": int(form.get("number-of-priority-levels"))
        }
        newDataset['settings'] = datasetSettings
        if form.get("number-of-processes") != None:
            lastArrive = 0
            arriveTime = 0
            for x in range(datasetSettings.get('numberOfProcesses')):
                if datasetSettings['randomizePriority']:
                    priority = randint(
                        1, datasetSettings['numberOfPriorityLevels'])
                else:
                    priority = 1
                if lastArrive == 0:
                    lastArrive += 1
                else:
                    arriveTime = randint(lastArrive, lastArrive + int(
                        (datasetSettings['processDispersionFactor']/100) * datasetSettings['maximumProcessDuration']))
                    lastArrive = arriveTime
                newDataset['data'].append({
                    "PID": x,
                    "arrive-time": arriveTime,
                    "period-time": randint(datasetSettings['minimumProcessDuration'], datasetSettings['maximumProcessDuration']),
                    "priority": priority
                })
        uniqueDatasetId = randint(10000, 99999)
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
