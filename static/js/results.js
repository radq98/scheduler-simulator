
$(document).ready(function () { 

    var data = JSON.parse(JSONdata);
    console.log(data)

    var toHide = document.getElementById('to-hide');
    var toUnhide = document.getElementById('to-unhide');

    function loadDataToParametersTable() {
        $('#parameterstable1 > tbody:last-child').append('<tr>');
        if (data.settings.algorithm != "") {
            $('#parameterstable1 > tbody:last-child').append('<td>' + data.settings.algorithm + '</td>');
        }
        if (data.settings.dataset != "") {
            $('#parameterstable1 > tbody:last-child').append('<td>' + data.settings.dataset + '</td>');
        }
        if (data.settings.dispatchLatency != "") {
            $('#parameterstable1 > tbody:last-child').append('<td>' + data.settings.dispatchLatency + '</td>');
        }
        else {
            $('#parameterstable1 > tbody:last-child').append('<td>Disabled</td>');
        }
        if (data.settings.rrInterval != "") {
            $('#parameterstable1 > tbody:last-child').append('<td>' + data.settings.rrInterval + '</td>');
        }
        else {
            $('#parameterstable1 > tbody:last-child').append('<td>---</td>');
        }
        if (data.settings.agingPriorities == "true") {
            $('#parameterstable1 > tbody:last-child').append('<td>Enabled</td>');
        }
        else {
            $('#parameterstable1 > tbody:last-child').append('<td>Disabled</td>');
        }
        if (data.settings.ppAgingInterval != "") {
            $('#parameterstable1 > tbody:last-child').append('<td>' + data.settings.ppAgingInterval + '</td>');
        }
        else {
            $('#parameterstable1 > tbody:last-child').append('<td>---</td>');
        }
        $('#parameterstable1 > tbody:last-child').append('</tr>');
    }

    function loadDataToSummaryTable() {
        $('#summarytable1 > tbody:last-child').append('<tr>');
        if (data.values[data.values.length-2].currentTime != "") {
            $('#summarytable1 > tbody:last-child').append('<td>' + data.values[data.values.length-2].currentTime + '</td>');
        }
        if (data.values[data.values.length-1].averageWaitingTime != "") {
            $('#summarytable1 > tbody:last-child').append('<td>' + data.values[data.values.length-1].averageWaitingTime + '</td>');
        }
        if (data.values[data.values.length-1].averageTurnaroundTime != "") {
            $('#summarytable1 > tbody:last-child').append('<td>' + data.values[data.values.length-1].averageTurnaroundTime + '</td>');
        }
        if (data.values[data.values.length-1].throughpul != "") {
            $('#summarytable1 > tbody:last-child').append('<td>' + data.values[data.values.length-1].throughpul + '</td>');
        }
        if (data.values[data.values.length-1].CPUusage != "") {
            $('#summarytable1 > tbody:last-child').append('<td>' + data.values[data.values.length-1].CPUusage + '</td>');
        }

        $('#parameterstable1 > tbody:last-child').append('</tr>');
    }
    function loadDataToCPUusageChart() {
        clearCPUusageChart();
        var color = getRandomColor();
        var newDataset = {
            label: "CPU usage",
            data: [],
            backgroundColor: color,
            borderColor: color,
            fill: false
        };
        CPUusageChart.data.datasets.push(newDataset);
        CPUusageChart.update();
        for (var ctx of data.values) {
            CPUusageChart.data.labels.push(ctx.currentTime);
            CPUusagePercent = Number(parseFloat(ctx.CPUusage)*100).toFixed(2);
            CPUusageChart.data.datasets[0].data.push(CPUusagePercent);
        }
        CPUusageChart.update();
    }

    function loadDataToThroughpulChart() {
        clearThroughpulChart();
        var color = getRandomColor();
        var newDataset = {
            label: "Throughpul",
            data: [],
            backgroundColor: color,
            borderColor: color,
            fill: false
        };
        ThroughpulChart.data.datasets.push(newDataset);
        ThroughpulChart.update();
        for (var ctx of data.values) {
            ThroughpulChart.data.labels.push(ctx.currentTime);
            ThroughpulChart.data.datasets[0].data.push(ctx.throughpul);
        }
        ThroughpulChart.update();
    }

    function loadDataToAverageWaitingTimeChart() {
        clearAverageWaitingTimeChart();
        var color = getRandomColor();
        var newDataset = {
            label: "Average Waiting Time",
            data: [],
            backgroundColor: color,
            borderColor: color,
            fill: false
        };
        AverageWaitingTimeChart.data.datasets.push(newDataset);
        AverageWaitingTimeChart.update();
        for (var ctx of data.values) {
            AverageWaitingTimeChart.data.labels.push(ctx.currentTime);
            AverageWaitingTimeChart.data.datasets[0].data.push(ctx.averageWaitingTime);
        }
        AverageWaitingTimeChart.update();
    }

    function loadDataToAverageTurnaroundTimeChart() {
        clearAverageTurnaroundTimeChart();
        var color = getRandomColor();
        var newDataset = {
            label: "Average Turnaround Time",
            data: [],
            backgroundColor: color,
            borderColor: color,
            fill: false
        };
        AverageTurnaroundTimeChart.data.datasets.push(newDataset);
        AverageTurnaroundTimeChart.update();
        for (var ctx of data.values) {
            AverageTurnaroundTimeChart.data.labels.push(ctx.currentTime);
            AverageTurnaroundTimeChart.data.datasets[0].data.push(ctx.averageWaitingTime);
        }
        AverageTurnaroundTimeChart.update();
    }
    
        if (data != null) {
            loadDataToParametersTable();
            loadDataToSummaryTable();
            loadDataToCPUusageChart();
            loadDataToThroughpulChart();
            loadDataToAverageWaitingTimeChart();
            loadDataToAverageTurnaroundTimeChart();
            toHide.hidden = true;
            toUnhide.hidden = false;
            $('body').css('height', 'auto');
        }
});