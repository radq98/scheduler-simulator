function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

function clearliveCPUusageChart()
    {
        var startLength = liveCPUusageChart.data.labels.length;
        for(i=0; i<startLength; i++)
        {
            liveCPUusageChart.data.labels.pop();
            liveCPUusageChart.data.datasets.forEach((dataset) => {
                dataset.data.pop();
            });
            //liveCPUusageChart.update();
        }
            liveCPUusageChart.data.datasets = [];
            //liveCPUusageChart.update();
        
    }


var liveCPUusageChartConfig = {
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
            text: 'CPU usage [%]',
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
                    labelString: '[%]',
                    fontColor: '#e5e5e5'
                }
            }]
        }
    }
};

var liveCPUusageChartContext = document.getElementById('liveCPUusageChartCanvas').getContext('2d');
var liveCPUusageChart = new Chart(liveCPUusageChartContext, liveCPUusageChartConfig);