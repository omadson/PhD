require(["http://d3js.org/d3.v3.js"], function (d3){
    d3.csv('data/rides_per_month_2015.csv', function(error, data) {
        data.forEach(function (d) {
            d.mes = +d.mes;
            d.M = +d['M'];
            d.F = +d['F'];
            d.O = +d['O'];
        });

        var chart = makeLineChart(data, 'mes', {
            'Feminino': {column: 'F'},
            'Masculino': {column: 'M'},
            'Outros': {column: 'O'},
        }, {xAxis: 'Mês', yAxis: 'Total de viagens'}, 400, 200, 'sexo');
        chart.bind("#rides_per_month_2015");
        chart.render();
    });

    d3.csv('data/rides_per_month_2016.csv', function(error, data) {
        data.forEach(function (d) {
            d.mes = +d.mes;
            d.M = +d['M'];
            d.F = +d['F'];
            d.O = +d['O'];
        });

        var chart = makeLineChart(data, 'mes', {
            'Feminino': {column: 'F'},
            'Masculino': {column: 'M'},
            'Outros': {column: 'O'},
        }, {xAxis: 'Mês', yAxis: 'Total de viagens'}, 400, 200, 'sexo');
        chart.bind("#rides_per_month_2016");
        chart.render();
    });

    d3.csv('data/rides_per_month_2017.csv', function(error, data) {
        data.forEach(function (d) {
            d.mes = +d.mes;
            d.M = +d['M'];
            d.F = +d['F'];
            d.O = +d['O'];
        });

        var chart = makeLineChart(data, 'mes', {
            'Feminino': {column: 'F'},
            'Masculino': {column: 'M'},
            'Outros': {column: 'O'},
        }, {xAxis: 'Mês', yAxis: 'Total de viagens'}, 400, 200, 'sexo');
        chart.bind("#rides_per_month_2017");
        chart.render();
    });
});