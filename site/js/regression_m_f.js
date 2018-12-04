require(["https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js"], function(d3){
    d3.csv('data/rides_per_sex.csv', function (error, data_) {

        formatDate = d3.time.format("%d/%m/%Y");
        formatP   = d3.format(".1f");
        function chordTip (d) {
            total = d.x + d.y;
            pM = 100 * (d.x / total);
            pF = 100 * (d.y / total);
            console.log(d)
            if (pM > pF) {
                return   `<strong>Data: ${formatDate(d.date)}</strong><br />
                                  Total: ${d.x + d.y} <br />
                                  Masculino: ${d.x} (${formatP(pM)}%)<br />
                                  Feminino: ${d.y} (${formatP(pF)}%)`;
            } else {
                return   `<strong>Data: ${formatDate(d.date)}</strong><br />
                                  Total: ${d.x + d.y} <br />
                                  Feminino: ${d.y} (${formatP(pF)}%)<br />
                                  Masculino: ${d.x} (${formatP(pM)}%)`;
            }
        }
        var margin = {
                top: 20,
                right: 20,
                bottom: 30,
                left: 40
            },
            width = 600 - margin.left - margin.right,
            height = 280 - margin.top - margin.bottom;

        var x = d3.scale.linear()
            .range([0, width]);

        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        var svg = d3.select("#regression_m_f").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var data = create_data(data_);

        var data_m = [];
        data.forEach(function(d) {
            d.x = +d.x;
            d.y = +d.y;
            d.yhat = +d.yhat;
            if (d.y > d.x) {
                data_m.push({'x': d.x, 'y': d.y});
            }
        });

        var line = d3.svg.line()
            .x(function(d) {
                return x(d.x);
            })
            .y(function(d) {
                return y(d.yhat);
            });

        x.domain(d3.extent(data, function(d) {
            return d.x;
        }));
        y.domain(d3.extent(data, function(d) {
            return d.y;
        }));

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .append("text")
            .attr("class", "label")
            .attr("x", width)
            .attr("y", -6)
            .style("text-anchor", "end")
            .text("Masculino");

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("class", "label")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Feminino");

        svg.selectAll(".dot2")
           .data(data_m)
           .enter().append("circle")
           .attr("class", "dot")
            .attr("r", 5.5)
            .attr("cx", function(d) {
                return x(d.x);
            })
            .attr("cy", function(d) {
                return y(d.y);
            })
            .style("stroke", "black")
            .style("stroke-width", 2);


        svg.selectAll(".dot")
            .data(data)
            .enter().append("circle")
            .attr("class", "dot")
            .attr("r", 3.5)
            .attr("cx", function(d) {
                return x(d.x);
            })
            .attr("cy", function(d) {
                return y(d.y);
            })
            .on("mouseover", function (d) {
                d3.select(this)
                  .style("fill", "#005824")
                  .style("stroke", "black")
                  .style("stroke-width", 2)
                  .attr('z-index', 1000)
                  .attr("r", 6.5);

                  d3.select(".tooltipleft")
                    .style("visibility", "visible")
                    .html(chordTip(d))
                    .style("top", function () { return (d3.event.pageY - 20)+"px"})
                    .style("left", function () { return (d3.event.pageX + 20)+"px";})
            })
            .on("mouseout", function (d) {
                d3.select(this)
                  .style("fill", 'rgba(0,88,36, 0.5)')
                  .style("stroke", 'none')
                  .attr('z-index', 0)
                  .attr("r", 3.5)
                d3.select(".tooltipleft").style("visibility", "hidden")
            });

        svg.append("path")
            .datum(data)
            .attr("class", "line")
            .attr("d", line);



        function create_data(data_) {
            var x = [];
            var y = [];
            var date = [];
            
            var x_mean = 0;
            var y_mean = 0;
            var term1 = 0;
            var term2 = 0;
            var noise_factor = 100;
            var noise = 0;
            // create x and y values
            ii = 0
            data_.forEach(function(d) {
                x.push(d.M_0);
                y.push(d.F_0);
                date.push(new Date(`${d.dia}T00:00:00.000-03:00`));
                x_mean += +d.M_0;
                y_mean += +d.F_0;

                ii+=1;
            });
            var n = ii;

            // for (var i = 0; i < n; i++) {
            //     noise = noise_factor * Math.random();
            //     noise *= Math.round(Math.random()) == 1 ? 1 : -1;
            //     y.push(i / 5 + noise);
            //     x.push(i + 1);
            //     x_mean += x[i]
            //     y_mean += y[i]
            // }
            // calculate mean x and y
            x_mean /= n;
            y_mean /= n;
            // calculate coefficients
            var xr = 0;
            var yr = 0;
            for (i = 0; i < x.length; i++) {
                xr = x[i] - x_mean;
                yr = y[i] - y_mean;
                term1 += xr * yr;
                term2 += xr * xr;

            }
            var b1 = term1 / term2;
            var b0 = y_mean - (b1 * x_mean);
            // perform regression 

            yhat = [];
            // fit line using coeffs
            for (i = 0; i < x.length; i++) {
                yhat.push(b0 + (x[i] * b1));
            }

            var data = [];
            for (i = 0; i < y.length; i++) {
                data.push({
                    "yhat": yhat[i],
                    "y": y[i],
                    "x": x[i],
                    "date": date[i]
                })
            }
            ff = d3.format('.1f');
            svg.append("g")
            .append("text")
            .attr("class", "label")
            .attr("x", width)
            .attr("y", height-20)
            .style("text-anchor", "end")
            .text("y = "+ff(b0)+" + "+ff(b1)+"x");

            return (data);
        }
    });
});