function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

function clearAverageTurnaroundTimeChart()
    {
        var startLength = AverageTurnaroundTimeChart.data.labels.length;
        for(i=0; i<startLength; i++)
        {
            AverageTurnaroundTimeChart.data.labels.pop();
            AverageTurnaroundTimeChart.data.datasets.forEach((dataset) => {
                dataset.data.pop();
            });
            //AverageTurnaroundTimeChart.update();
        }
            AverageTurnaroundTimeChart.data.datasets = [];
            //AverageTurnaroundTimeChart.update();
        
    }


var AverageTurnaroundTimeChartConfig = {
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
            text: 'Average Turnaround Time',
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

var AverageTurnaroundTimeChartContext = document.getElementById('AverageTurnaroundTimeChartCanvas').getContext('2d');
var AverageTurnaroundTimeChart = new Chart(AverageTurnaroundTimeChartContext, AverageTurnaroundTimeChartConfig);