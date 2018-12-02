require(["http://d3js.org/d3.v3.js"], function (d3){
    d3.csv('data/rides_per_hour.csv', function(error, data) {
        data.forEach(function (d) {
            d.mes = +d.hora;
            d.M = +d['dia útil'];
            d.F = +d['dia não útil'];
        });

        var chart = makeLineChart(data, 'mes', {
            'Dias úteis': {column: 'M'},
            'Feriados e finais de semana': {column: 'F'},
        }, {xAxis: 'Horário de retirada', yAxis: 'Média de viagens'}, 800, 300,'hora');
        chart.bind("#rides_per_hour");
        chart.render();
    });
});