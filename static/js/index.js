$(function () {
    const colors = ['#f56954', '#00a65a', '#f39c12', '#00c0ef',
        '#575abc', '#220d2b', '#c2f2f7', '#a92588', '#579b4c',
        '#ceb51a', '#851421', '#0879ae', '#1f1d32', '#eb7c59', '#3c02aa']
    //-------------
    //- DONUT CHART -
    //-------------
    var donutChartCanvas = $('#donutChart').get(0).getContext('2d')
    let h3CategoriesTitle = $('.category-title')
    var donutData = {
        labels: jQuery.map(h3CategoriesTitle, function (e) { return jQuery(e).html() }),
        datasets: [
            {
                data: jQuery.map(h3CategoriesTitle, function (e) { return jQuery(e).data("sum-expenses") }),
                backgroundColor: colors.slice(0, h3CategoriesTitle.length),
            }
        ]
    }
    var donutOptions = {
        legend: { display: true },
        maintainAspectRatio: false,
        responsive: true,
        tooltips: {
            callbacks: {
                label: function (tooltipItem, data) {
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                    var total = meta.total;
                    var currentValue = dataset.data[tooltipItem.index];
                    var percentage = parseFloat((currentValue / total * 100).toFixed(1));
                    return currentValue + ' (' + percentage + '%)';
                },
                title: function (tooltipItem, data) {
                    return data.labels[tooltipItem[0].index];
                }
            }
        },
    }
    var donutChart = new Chart(donutChartCanvas, {
        type: 'doughnut',
        data: donutData,
        options: donutOptions,
    })

    //-------------
    //- BAR CHART -
    //-------------
    var barChartData = {
        labels: ["Monthly Expenses", "Monthly Income"],
        datasets: [
            {
                backgroundColor: ["#c41f1f", "#2f84d4"],
                data: [$("#monthly-expenses").val(), $("#monthly-income").val()],
                minBarLength: 2,
            }
        ]
    }

    var barChartCanvas = $('#barChart').get(0).getContext('2d')

    var barChartOptions = {
        scales: {
            yAxes: [{
                gridLines: {
                    display: false
                },
                ticks: {
                    beginAtZero: true
                }
            }],
            xAxes: [{
                gridLines: {
                    display: false,
                }
            }]
        },
        label: true,
        legend: { display: false },
        responsive: true,
        maintainAspectRatio: false,
        datasetFill: false,
    }

    var barChart = new Chart(barChartCanvas, {
        type: 'bar',
        data: barChartData,
        options: barChartOptions,
    })
});