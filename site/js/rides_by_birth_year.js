require(['https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js'], function (d3) {
  d3.csv("data/perc_num_of_rides_per_birth_year.csv", function (data) {

    data.forEach(function(d){   
      d.Homens = d.M;
      d.Mulheres = d.F;

      // if (d.O == ""){
      //   d.O = 0
      // }  else{
      //   d.O = +d.O;  
      // }    
      d.O = +d.O;  
      d.Outros= d.O.toString(); 
      d.Ano = d.year;
    });

    var margin = {top: 20, right: 140, bottom: 35, left: 30};

    var width = 1170 - margin.left - margin.right,
        height = 320 - margin.top - margin.bottom;

    var svg = d3.select("#rides_by_birth_year")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
   

    var parse = d3.time.format("%Y").parse;

    // Transpose the data into layers
    var dataset = d3.layout.stack()(["Homens", "Mulheres", "Outros"].map(function(sexo) {
      return data.map(function(d) {
        return {x: parse(d.Ano), y: +d[sexo]};
      });
    }));

    // Set x, y and colors
    var x = d3.scale.ordinal()
      .domain(dataset[0].map(function(d) { return d.x; }))
      .rangeRoundBands([10, width-10], 0.02);

    var y = d3.scale.linear()
      .domain([0, d3.max(dataset, function(d) {  return d3.max(d, function(d) { return d.y0 + d.y; });  })])
      .range([height, 0]);


    var fm = d3.format(".1f");

    // function segColor(c){ return {M:"#d95f02", F:"#1b9e77",O:"#7570b3"}[c]; }
           
    var colors = ["#1b9e77", "#d95f02", "#7570b3"];
    
    // Define and draw axes
    var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(12)
      .tickSize(-width, 0, 0)
      .tickFormat( function(d) { return fm(d) } );

    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")    
      .tickFormat(d3.time.format("%Y"));   

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(-12," + (height+15) + ")")    
      .call(xAxis)
      .selectAll("text")
        .attr("transform", "rotate(-90)");


    // Create groups for each series, rects for each segment 
    var groups = svg.selectAll("g.cost")
      .data(dataset)
      .enter().append("g")
      .attr("class", "cost")
      .style("fill", function(d, i) { return colors[i]; });

    var rect = groups.selectAll("rect")
      .data(function(d) { return d; })
      .enter()
      .append("rect")
      .attr("x", function(d) { return x(d.x); })
      .attr("y", function(d) { return y(d.y0 + d.y); })
      .attr("height", function(d) { return y(d.y0) - y(d.y0 + d.y); })
      .attr("width", x.rangeBand()-1)
      .on("mouseover", function() { tooltip.style("display", null); })
      .on("mouseout", function() { tooltip.style("display", "none"); })
      .on("mousemove", function(d) {
        var xPosition = d3.mouse(this)[0] - 15;
        var yPosition = d3.mouse(this)[1] - 25;
        tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
        tooltip.select("text").text(fm(d.y)+'%');
      });


    // Draw legend
    var legend = svg.selectAll(".legend")
      .data(colors)
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });
     
    legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", function(d, i) {return colors.slice().reverse()[i];});
     
    legend.append("text")
      .attr("x", width + 5)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "start")
      .text(function(d, i) { 
        switch (i) {
          case 0: return "Outros";
          case 1: return "Feminino";        
          case 2: return "Masculino";
          // case 3: return "Red Delicious apples";
        }
      });


    // Prep the tooltip bits, initial display is hidden
    var tooltip = svg.append("g")
      .attr("class", "tooltip_a")
      .style("display", "none");
        
    tooltip.append("rect")
      .attr("width", 40)
      .attr("height", 20)
      .attr("fill", "white")
      .style("opacity", 0.5);

    tooltip.append("text")
      .attr("x", 20)
      .attr("dy", "1.2em")
      .style("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("font-weight", "bold");

  });  
});