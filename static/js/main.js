$(document).ready(function () { 

    var formObjects = {
        algorithm: document.getElementById("form-algorithm"),
        dataset: document.getElementById("form-dataset"),
        visualization: document.getElementById("form-visualization"),
        rrInterval: document.getElementById("form-rr-interval"),
        agingPriorities: document.getElementById("form-aging-priorities"),
        ppAgingInterval: document.getElementById("form-pp-aging-interval"),
        ppDiv: document.getElementById("form-PP-div"),
        rrDiv: document.getElementById("form-RR-div")
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
});
