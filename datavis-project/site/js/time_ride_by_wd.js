require(["https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"], function (d3){
    d3.csv('data/time_ride_by_wd.csv', function(error, data) {
        data.forEach(function (d) {
            d.mes = +d.minutos;
            d.M = +d['dia útil'];
            d.F = +d['dia não útil'];
        });
        var chart = makeLineChart(data, 'mes', {
            'Dias úteis': {column: 'M'},
            'Feriados e finais de semana': {column: 'F'},
        }, {xAxis: 'Minutos', yAxis: 'Média de viagens'}, 500, 250,'hora');
        chart.bind("#time_ride_by_wd");
        chart.render();
    });
});