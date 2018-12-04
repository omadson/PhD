require(["http://d3js.org/d3.v3.js"], function (d3){
    d3.csv('data/time_ride_by_sex.csv', function(error, data) {
        data.forEach(function (d) {
            d.mes = +d.minutos;
            d.M = +d['M'];
            d.F = +d['F'];
            d.O = +d['O'];
        });

        var chart = makeLineChart(data, 'mes', {
            'Feminino': {column: 'F'},
            'Masculino': {column: 'M'},
            'Outros': {column: 'O'},
        }, {xAxis: 'Minutos', yAxis: 'Total de viagens'}, 680, 200, 'sexo');
        chart.bind("#time_ride_by_sex");
        chart.render();
    });

});