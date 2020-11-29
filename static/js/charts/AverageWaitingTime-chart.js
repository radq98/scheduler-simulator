function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

function clearAverageWaitingTimeChart()
    {
        var startLength = AverageWaitingTimeChart.data.labels.length;
        for(i=0; i<startLength; i++)
        {
            AverageWaitingTimeChart.data.labels.pop();
            AverageWaitingTimeChart.data.datasets.forEach((dataset) => {
                dataset.data.pop();
            });
            //AverageWaitingTimeChart.update();
        }
            AverageWaitingTimeChart.data.datasets = [];
            //AverageWaitingTimeChart.update();
        
    }


var AverageWaitingTimeChartConfig = {
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
            text: 'Average Waiting Time',
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

var AverageWaitingTimeChartContext = document.getElementById('AverageWaitingTimeChartCanvas').getContext('2d');
var AverageWaitingTimeChart = new Chart(AverageWaitingTimeChartContext, AverageWaitingTimeChartConfig);