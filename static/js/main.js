$(document).ready(function () { 
    var formRRdiv = document.getElementById("form-RR-div");
    var formPPdiv = document.getElementById("form-PP-div");
    var formDataset = document.getElementById("form-dataset");
    var formAlgorythm = document.getElementById("form-algorythm");

    
    $('#form-algorythm').change(function(){
        if (formAlgorythm.value == "Round Robin") {
            formRRdiv.hidden = false;
            formPPdiv.hidden = true;
        }
        else if (formAlgorythm.value == "Priority planning") {
            formRRdiv.hidden = true;
            formPPdiv.hidden = false;
        }
        else {
            formRRdiv.hidden = true;
            formPPdiv.hidden = true;
        }
    });
});
