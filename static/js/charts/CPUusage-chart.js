function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

function clearCPUusageChart()
    {
        var startLength = CPUusageChart.data.labels.length;
        for(i=0; i<startLength; i++)
        {
            CPUusageChart.data.labels.pop();
            CPUusageChart.data.datasets.forEach((dataset) => {
                dataset.data.pop();
            });
            //CPUusageChart.update();
        }
            CPUusageChart.data.datasets = [];
            //CPUusageChart.update();
        
    }


var CPUusageChartConfig = {
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

var CPUusageChartContext = document.getElementById('CPUusageChartCanvas').getContext('2d');
var CPUusageChart = new Chart(CPUusageChartContext, CPUusageChartConfig);