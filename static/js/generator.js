$(document).ready(function () { 
    var formRandomizePriority = document.getElementById("form-randomize-priority");
    var formNumberOfPriorityLevels = document.getElementById("form-number-of-priority-levels");

    $('#form-randomize-priority').change(function(){
        console.log(formRandomizePriority.checked);
        if (formRandomizePriority.checked) {
            formNumberOfPriorityLevels.disabled = false;
        }
        else {
            formNumberOfPriorityLevels.disabled = true;
        }
    });
});
