function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

function clearLiveWaitingTimeChart()
    {
        var startLength = liveWaitingTimeChart.data.labels.length;
        for(i=0; i<startLength; i++)
        {
            liveWaitingTimeChart.data.labels.pop();
            liveWaitingTimeChart.data.datasets.forEach((dataset) => {
                dataset.data.pop();
            });
            liveWaitingTimeChart.update();
        }
            liveWaitingTimeChart.data.datasets = [];
            liveWaitingTimeChart.update();
        
    }

function doSamplesLimit(sampleslimit) {
    if(sampleslimit.value!="Unlimited")
    {
        var maxsamples = parseInt(sampleslimit.value);
        if (liveWaitingTimeChart.data.labels.length>maxsamples){
            for(var i=0; i<liveWaitingTimeChart.data.datasets.length;i++) {
                if(liveWaitingTimeChart.data.datasets[i].data.length > maxsamples) {
                    liveWaitingTimeChart.data.datasets[i].data.shift();
                }
            }
            liveWaitingTimeChart.data.labels.shift();
            liveWaitingTimeChart.update(0);
        }
    }
}

var liveWaitingTimeChartConfig = {
    type: 'line',
    data: {
        datasets: [],
    },
    options: {
        legend: {
            labels: {
                 fontColor: '#e5e5e5'
                }
             },
        responsive: true,
        title: {
            display: true,
            text: 'Average waiting time',
            fontColor: '#e5e5e5'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'point',
            intersect: false
        },
        scales: {
            xAxes: [{
                ticks: {
                    fontColor: '#e5e5e5',
                    maxTicksLimit: 15
                },
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Time',
                    fontColor: '#e5e5e5'
                }
            }],
            yAxes: [{
                ticks: {
                    fontColor: '#e5e5e5'
                },
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '[time unit]',
                    fontColor: '#e5e5e5'
                }
            }]
        }
    }
};

var liveWaitingTimeChartContext = document.getElementById('liveWaitingTimeChartCanvas').getContext('2d');
var liveWaitingTimeChart = new Chart(liveWaitingTimeChartContext, liveWaitingTimeChartConfig);