function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

function clearThroughpulChart()
    {
        var startLength = ThroughpulChart.data.labels.length;
        for(i=0; i<startLength; i++)
        {
            ThroughpulChart.data.labels.pop();
            ThroughpulChart.data.datasets.forEach((dataset) => {
                dataset.data.pop();
            });
            //ThroughpulChart.update();
        }
            ThroughpulChart.data.datasets = [];
            //ThroughpulChart.update();
        
    }


var ThroughpulChartConfig = {
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
            text: 'Troughpul',
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
                    labelString: '[processes/1 time unit]',
                    fontColor: '#e5e5e5'
                }
            }]
        }
    }
};

var ThroughpulChartContext = document.getElementById('ThroughpulChartCanvas').getContext('2d');
var ThroughpulChart = new Chart(ThroughpulChartContext, ThroughpulChartConfig);