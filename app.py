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

@app.route('/_get_results')
def get_results():
    simulationSettings = {
        "algorithm": request.args.get('algorithm', None, type=str),
        "dataset": request.args.get('dataset', None, type=str),
        "visualization": request.args.get('visualization', None, type=str),
        "rrInterval": request.args.get('rrInterval', None, type=str),
        "agingPriorities": request.args.get('agingPriorities', None, type=str),
        "ppAgingInterval": request.args.get('ppAgingInterval', None, type=str),
        "dispatchLatency": request.args.get('dispatchLatency', None, type=int)
    }
    dataset = None
    with open("./datasets/" + simulationSettings['dataset'], "r") as f:
        dataset = json.load(f)
    
    steps = []
    values = []

    #scheduling FCFS
    def newStep(time, eventType, PID):
        return {"time": time, "eventType": eventType, "PID": PID}
    
    def newValue(currentTime, toProcessCount, processedCount, queueList, processingList, processedList, averageWaitingTime, averageTurnaroundTime, throughpul, CPUusage):
        return {"currentTime": currentTime, 
        "toProcessCount": toProcessCount, 
        "processedCount": processedCount, 
        "queueList": queueList, 
        "processingList": processingList, 
        "processedList": processedList, 
        "averageWaitingTime": round(averageWaitingTime,3), 
        "averageTurnaroundTime": round(averageTurnaroundTime,3),
        "throughpul": round(throughpul, 3),
        "CPUusage": round(CPUusage, 3)}
    currentTime = 0
    currentProcess = None
    toProcessCount = dataset['settings']['numberOfProcesses']
    processedCount = 0
    queueList = dataset['data']
    initialQueueListLen = len(queueList)
    #adding necessary parameters to process objects
    for x in queueList:
        x["waitingTime"] = 0
        x["turnaroundTime"] = 0
    averageWaitingTime = 0
    averageTurnaroundTime = 0
    throughpul = 0
    CPUusage = 0
    timeWithTasks = 0
    timeWithoutTasks = 0
    dispatchingTime = 0
    processingList = []
    processedList = []
    toRemoveFromQueue = []
    steps.append(newStep(currentTime, "simulation-start", None))
    values.append(newValue("start", toProcessCount, processedCount, queueList.copy(), processingList.copy(), processedList.copy(), averageWaitingTime, averageTurnaroundTime, throughpul, CPUusage))
    
    dispatching = False
    currentDispatchTime = 0

    processShiftLock = False

    
    if simulationSettings["algorithm"] == "Round Robin":
        rrCurrent = 0
        rrIntervalControl = int(simulationSettings["rrInterval"])

    while toProcessCount > 0:
       # print("currentTime " + str(currentTime))
       # print("queueList " + str(len(queueList)))
       # print("processingList " + str(len(processingList)))
       # print("processedList " + str(len(processedList)))
       # print("toProcessCount " + str(toProcessCount))
       # print(steps[-1])
       # if len(processingList) > 0:
       #     print("processingList[-1]['period-time'] " + str(processingList[-1]['period-time']))
       # print(" ")
        for x in queueList:
            if int(x['arrive-time']) == int(currentTime):
                processingList.append(x.copy())
                toRemoveFromQueue.append(x)
                steps.append(newStep(currentTime, "arrive", str(processingList[-1]['PID'])))
                if (len(processingList) == 1) and (simulationSettings['dispatchLatency'] > 0):
                    dispatching = True
                    currentDispatchTime = simulationSettings['dispatchLatency']
        for x in toRemoveFromQueue:
            queueList.remove(x)
        toRemoveFromQueue = []
            
        if (len(processingList) > 0) and (dispatching == False):
            timeWithTasks += 1
            for x in processingList:
                x['turnaroundTime'] += 1
            if simulationSettings["algorithm"] == "FCFS":   
                currentProcess = processingList[0]
                if len(processingList) > 1:
                    for x in processingList:
                        if x != currentProcess:
                            x['waitingTime'] += 1
                steps.append(newStep(currentTime, "processing", str(processingList[0]['PID'])))
                processingList[0]['period-time'] -= 1
                if processingList[0]['period-time'] == 0:
                    processedList.append(processingList[0].copy())
                    steps.append(newStep(currentTime, "finished", str(processingList[0]['PID'])))
                    processingList.pop(0)
                    toProcessCount -= 1
                    processedCount += 1
                    if (len(processingList) >= 1) and (simulationSettings['dispatchLatency'] > 0):
                        dispatching = True
                        currentDispatchTime = simulationSettings['dispatchLatency']
                if toProcessCount>0:
                    currentTime += 1
            
            elif simulationSettings["algorithm"] == "Round Robin":    
                currentProcess = processingList[rrCurrent]
                if len(processingList) > 1:
                    for x in processingList:
                        if x != currentProcess:
                            x['waitingTime'] += 1
                steps.append(newStep(currentTime, "processing", str(processingList[rrCurrent]['PID'])))
                processingList[rrCurrent]['period-time'] -= 1
                rrIntervalControl -= 1

                if processingList[rrCurrent]['period-time'] == 0:
                    processedList.append(processingList[rrCurrent].copy())
                    steps.append(newStep(currentTime, "finished", str(processingList[rrCurrent]['PID'])))
                    processingList.pop(rrCurrent)
                    toProcessCount -= 1
                    processedCount += 1
                    rrCurrent -= 1
                    rrIntervalControl = 0
                    if (len(processingList) >= 1) and (simulationSettings['dispatchLatency'] > 0):
                        dispatching = True
                        currentDispatchTime = simulationSettings['dispatchLatency']
                
                if rrIntervalControl == 0:
                    if rrCurrent < len(processingList)-1:
                        rrCurrent += 1
                    else:
                        rrCurrent = 0
                    rrIntervalControl = int(simulationSettings["rrInterval"])
                if toProcessCount>0:
                    currentTime += 1
            
            elif simulationSettings["algorithm"] == "Priority planning":
                if processShiftLock == False:
                    maxPriorityProcessId=0
                    maxPriority=9999999
                    for x in processingList:
                        if(x["priority"]<maxPriority):
                            maxPriority = x["priority"]
                            maxPriorityProcessId = processingList.index(x)
                            print("maxPriority: " + str(maxPriority))
                            print("maxPriorityProcessId: " + str(maxPriorityProcessId))
                    processShiftLock = True
                currentProcess = processingList[maxPriorityProcessId]
                if len(processingList) > 1:
                    for x in processingList:
                        if x != currentProcess:
                            x['waitingTime'] += 1
                steps.append(newStep(currentTime, "processing", str(processingList[maxPriorityProcessId]['PID'])))

                processingList[maxPriorityProcessId]['period-time'] -= 1

                if processingList[maxPriorityProcessId]['period-time'] == 0:
                    processedList.append(processingList[maxPriorityProcessId].copy())
                    steps.append(newStep(currentTime, "finished", str(processingList[maxPriorityProcessId]['PID'])))
                    processingList.pop(maxPriorityProcessId)
                    toProcessCount -= 1
                    processedCount += 1
                    processShiftLock = False
                    if (len(processingList) >= 1) and (simulationSettings['dispatchLatency'] > 0):
                        dispatching = True
                        currentDispatchTime = simulationSettings['dispatchLatency']
                if toProcessCount>0:
                    currentTime += 1
            if(simulationSettings['dispatchLatency'] == 0):
                dispatching = False
        else:
            if(dispatching == True):
                currentDispatchTime -= 1
                dispatchingTime +=1
                steps.append(newStep(currentTime, "dispatch-latency", None))
                if(currentDispatchTime == 0):
                    dispatching = False
            else:
                steps.append(newStep(currentTime, "no-task", None))

            timeWithoutTasks += 1
            if simulationSettings["algorithm"] == "Round Robin":   
                rrCurrent = 0
                rrIntervalControl = int(simulationSettings["rrInterval"])
            currentTime += 1
        
        CPUusage = timeWithTasks / (timeWithTasks + timeWithoutTasks)
        averageWaitingTimeSum = 0
        averageTurnaroundTimeSum = 0
        for x in processingList:
            averageWaitingTimeSum += int(x["waitingTime"])
            averageTurnaroundTimeSum += int(x["turnaroundTime"])
        for x in processedList:
            averageWaitingTimeSum += int(x["waitingTime"])
            averageTurnaroundTimeSum += int(x["turnaroundTime"])
        if (len(processingList) + len(processedList)) != 0:
            averageWaitingTime = averageWaitingTimeSum / (len(processingList) + len(processedList))
            averageTurnaroundTime = averageTurnaroundTimeSum / (len(processingList) + len(processedList))
        else:
            averageWaitingTime = 0
        
        throughpul = len(processedList)/currentTime

        values.append(newValue(currentTime, toProcessCount, processedCount, queueList.copy(), processingList.copy(), processedList.copy(), averageWaitingTime, averageTurnaroundTime, throughpul, CPUusage))  

    steps.append(newStep(currentTime, "simulation-finished", None))
    values.append(newValue("finished", toProcessCount, processedCount, queueList.copy(), processingList.copy(), processedList.copy(), averageWaitingTime, averageTurnaroundTime, throughpul, CPUusage))
    results = {
        "settings": simulationSettings,
        "steps": steps,
        "values": values.copy()
    }

    uniqueDatasetId = randint(10000, 99999)
    datenow = datetime.now().date()
    if results != []:
        with open("./results/result-"+str(datenow)+"-"+str(uniqueDatasetId)+".json", "w",) as f:
            json.dump(results, f, indent=4)

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
    list = os.listdir("./results/")
    selectedResult = None
    data = None

    arg = request.args

    if request.method == "GET":
        if(arg.get("id") == None):
            selectedResult = None
        else: 
            selectedResult = arg.get("id")
            with open("./results/" + selectedResult, "r") as f:
                data = json.load(f)
        
        


    context = {
        "appversion": appversion,
        "footertext": footertext,
        "list": list,
        "selectedResult": selectedResult,
        "data": data
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
