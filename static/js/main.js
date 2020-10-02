$(document).ready(function () { 

    var formObjects = {
        algorithm: document.getElementById("form-algorithm"),
        dataset: document.getElementById("form-dataset"),
        visualization: document.getElementById("form-visualization"),
        rrInterval: document.getElementById("form-rr-interval"),
        agingPriorities: document.getElementById("form-aging-priorities"),
        ppAgingInterval: document.getElementById("form-pp-aging-interval"),
        ppDiv: document.getElementById("form-PP-div"),
        rrDiv: document.getElementById("form-RR-div"),
        startButton: document.getElementById("start-button"),
        dispatchLatency: document.getElementById("form-dispatch-latency")
      }

    
    $('#form-algorithm').change(function(){
        if (formObjects.algorithm.value == "Round Robin") {
            formObjects.rrDiv.hidden = false;
            formObjects.ppDiv.hidden = true;
        }
        else if (formObjects.algorithm.value == "Priority planning") {
            formObjects.rrDiv.hidden = true;
            formObjects.ppDiv.hidden = false;
        }
        else {
            formObjects.rrDiv.hidden = true;
            formObjects.ppDiv.hidden = true;
        }
    });

    //poka-yoke functions
    function FormLock() {
        formObjects.algorithm.disabled = true;
        formObjects.dataset.disabled = true;
        formObjects.visualization.disabled = true;
        formObjects.rrInterval.disabled = true;
        formObjects.agingPriorities.disabled = true;
        formObjects.ppAgingInterval.disabled = true;
        formObjects.startButton.disabled = true;
    }

    function FormUnlock() {
        formObjects.algorithm.disabled = false;
        formObjects.dataset.disabled = false;
        formObjects.visualization.disabled = false;
        formObjects.rrInterval.disabled = false;
        formObjects.agingPriorities.disabled = false;
        formObjects.ppAgingInterval.disabled = false;
        formObjects.startButton.disabled = false;
    }

    $('#start-button').on('click', function (event) {
        console.log("Begin test");
        if (formObjects.visualization.checked) {
            FormLock();
        } 
    });

    var invalidChars = [
        "-",
        "+",
        "e",
        "E",
        ".",
        ","
    ];

    formObjects.rrInterval.min = 1;
    formObjects.rrInterval.max = 3600;
    formObjects.rrInterval.step = 1;
    $('#form-rr-interval').on('keyup', function () {
        if (parseFloat(this.value) > formObjects.rrInterval.max) { this.value = formObjects.rrInterval.max; return false; };
        if (parseFloat(this.value) < formObjects.rrInterval.min) { this.value = formObjects.rrInterval.min; return false; };
        if (parseFloat(this.value) != parseInt(this.value)) { this.value = parseFloat(this.value).toFixed(0); };
    });

    formObjects.rrInterval.addEventListener("keydown", function (e) {
        if (invalidChars.includes(e.key)) {
            e.preventDefault();
        }
    });

    formObjects.ppAgingInterval.min = 1;
    formObjects.ppAgingInterval.max = 3600;
    formObjects.ppAgingInterval.step = 1;
    $('#form-pp-aging-interval').on('keyup', function () {
        if (parseFloat(this.value) > formObjects.ppAgingInterval.max) { this.value = formObjects.ppAgingInterval.max; return false; };
        if (parseFloat(this.value) < formObjects.ppAgingInterval.min) { this.value = formObjects.ppAgingInterval.min; return false; };
        if (parseFloat(this.value) != parseInt(this.value)) { this.value = parseFloat(this.value).toFixed(0); };
    });

    formObjects.ppAgingInterval.addEventListener("keydown", function (e) {
        if (invalidChars.includes(e.key)) {
            e.preventDefault();
        }
    });

    formObjects.dispatchLatency.min = 0;
    formObjects.dispatchLatency.max = 3600;
    formObjects.dispatchLatency.step = 1;
    $('#form-dispatch-latency').on('keyup', function () {
        if (parseFloat(this.value) > formObjects.dispatchLatency.max) { this.value = formObjects.dispatchLatency.max; return false; };
        if (parseFloat(this.value) < formObjects.dispatchLatency.min) { this.value = formObjects.dispatchLatency.min; return false; };
        if (parseFloat(this.value) != parseInt(this.value)) { this.value = parseFloat(this.value).toFixed(0); };
    });

    formObjects.dispatchLatency.addEventListener("keydown", function (e) {
        if (invalidChars.includes(e.key)) {
            e.preventDefault();
        }
    });

});

