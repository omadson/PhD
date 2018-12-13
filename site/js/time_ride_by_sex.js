require(["https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"], function (d3){
    d3.csv('data/time_ride_by_sex.csv', function(error, data) {
        
        let totalM = d3.sum(data, function(d) { return +d.M; });
        let totalF = d3.sum(data, function(d) { return +d.F; });
            // let totalO = d3.sum(data, function(d) { return +d.O; });        

        data.forEach(function (d) {
            d.mes = +d.minutos;
            d.M = (+d['M']/totalM)*100;
            d.F = (+d['F']/totalF)*100;
            // d.O = (+d['O']/totalO)*100;
            data
        });

        var chart = makeLineChart(data, 'mes', {
            'Feminino': {column: 'F'},
            'Masculino': {column: 'M'},
            // 'Outros': {column: 'O'},
        }, {xAxis: 'Minutos', yAxis: 'Total das viagens (%)'}, 680, 200, 'time_ride_sexo');
        chart.bind("#time_ride_by_sex");
        chart.render();
    });

});