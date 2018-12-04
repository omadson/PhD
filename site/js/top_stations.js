require(['https://d3js.org/d3.v4.min.js'], function(d3) {

  // dataset = {"children": []};
  // d3.csv("data/top_count_stations.csv", function(data) {
  //   data.forEach(function (d) {
  //     dataset["children"].push({"Name": d.neighborhood, "Count": +d.bicicletar});
  //   })
  // });
  // dataset = {"children": dd};
  // dataset = {"children": [{"Name": 'Aldeota', "Count": 11},
  //                         {"Name": 'Centro', "Count": 10},
  //                         {"Name": 'Meireles', "Count": 8},
  //                         {"Name": 'Cocó', "Count": 6},
  //                         {"Name": 'Fátima', "Count": 5},
  //                         {"Name": 'Papicu', "Count": 4},
  //                         {"Name": 'Farias Brito', "Count": 3},
  //                         {"Name": 'Patriolino Ribeiro', "Count": 3},
  //                         {"Name": 'Dionísio Torres', "Count": 3}]}
  dataset = {"children": [{"Name": 'Aldeota', "Count": 11},
                          {"Name": 'Centro', "Count": 10},
                          {"Name": 'Meireles', "Count": 8},
                          {"Name": 'Cocó', "Count": 6},
                          {"Name": 'Fátima', "Count": 5},
                          {"Name": 'Papicu', "Count": 4},
                          {"Name": 'Dionísio Torres', "Count": 3},
                          {"Name": 'Farias Brito', "Count": 3},
                          {"Name": 'Patriolino Ribeiro', "Count": 3},
                          {"Name": 'Monte Castelo', "Count": 2},
                          {"Name": 'JOSE BONIFACIO', "Count": 2},
                          {"Name": 'PARQUELANDIA', "Count": 2},
                          {"Name": 'RODOLFO TEOFILO', "Count": 2},
                          {"Name": 'JOAQUIM TAVORA', "Count": 2},
                          {"Name": 'GENTILANDIA', "Count": 2},
                          {"Name": 'BOM FUTURO', "Count": 2},
                          {"Name": 'PICI', "Count": 1},
                          {"Name": 'DAMAS', "Count": 1},
                          {"Name": 'MONTESE', "Count": 1},
                          {"Name": 'JACARECANGA', "Count": 1},
                          {"Name": 'JARDIM AMERICA', "Count": 1},
                          {"Name": 'SAO GERARDO', "Count": 1},
                          {"Name": 'PRAIA DE IRACEMA', "Count": 1},
                          {"Name": 'PRESIDENTE KENNEDY', "Count": 1},
                          {"Name": 'ENG LUCIANO CAVALCANTE', "Count": 1},
                          {"Name": 'AMADEU FURTADO', "Count": 1},
                          {"Name": 'BENFICA', "Count": 1},
                          {"Name": 'São João do Tauape', "Count": 1},
                          {"Name": 'PARREAO', "Count": 1},
                          {"Name": 'EDSON QUEIROZ', "Count": 1}]}
  
  // var color = d3.scaleOrdinal(d3.schemeCategory20);
  // let blues = d3.quantize(d3.interpolateGreens, 5);
  // let blues = ['#fff', '#f7fcb9', '#addd8e', '#78c679', '#41ab5d', '#238443', '#006837', '#004529']
  let blues = ['#f7fcb9', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#005a32'].reverse()
  let color = d3.scaleQuantile().domain([0,1,2,5,10,12]).range(blues);

  var diameter = 450;
  // var color = d3.scaleOrdinal(d3.schemeCategory20);

  var bubble = d3.pack(dataset)
      .size([diameter, diameter])
      .padding(1.5);

  var svg = d3.select("#top_stations")
      .append("svg")
      .attr("width", diameter)
      .attr("height", diameter)
      .attr("class", "bubble");

  var nodes = d3.hierarchy(dataset)
      .sum(function(d) { 
        return d.Count; });
  var node = svg.selectAll(".node")
      .data(bubble(nodes).descendants())
      .enter()
      .filter(function(d){
          return  !d.children
      })
      .append("g")
      .attr("class", "node")
      .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
      });

  // node.append("title")
  //     .text(function(d) {
  //         return d.Name + ": " + d.Count;
  //     });

  node.append("circle")
      .attr("r", function(d) {
          return d.r;
      })
      .style("fill", function(d,i) {
          return color(i);
      });

  node.append("text")
      .attr("dy", ".2em")
      .style("text-anchor", "middle")
      .text(function(d) {
          if (d.r > 34) {
            return d.data.Name.substring(0, d.r / 2);
          } else {
            return ''
          }
      })
      .attr("font-family", "sans-serif")
      .attr("font-size", function(d){
          return d.r/5;
      })
      .attr("fill", "black");

  node.append("text")
      .attr("dy", "1.3em")
      .style("text-anchor", "middle")
      .text(function(d) {
          if (d.r > 34) {
            return d.data.Count;
          }  else {
            return '';
          }
      })
      .attr("font-size", function(d){
          return d.r/5;
      })
      .attr("fill", "black");

  d3.select(self.frameElement)
      .style("height", diameter + "px");



});
// require(['https://d3js.org/d3.v4.min.js'], function(d3) {
//   formatP   = d3.format(".1f");
//   function chordTip (d) {
//       total = 80;
//       pM = 100 * (d.value / total);
//       return `Estações: ${+d.value} (${formatP(pM)}%)`;
//   }
//   var  width = 900,
//       height = 900;

//   var svg = d3.select("#top_stations")
//               .append("svg")
//               .attr("width", width)
//               .attr("height", height);      
//   // Define the div for the tooltip
//   var div = d3.select(".tooltipleft");

//   //svg.append("text")
//     //.attr("x", 100)   
//       //.attr("y", 20 )
//       //.attr("dy", "3.5em" )
//       //.attr("text-anchor", "start")  
//       //.style("font-size", "28px")  
//         //.style("font-weight", "bold")
//       //.text("SFFD Call Incidents in December 2016 ")

//   var pack = d3.pack()
//       .size([width, height])
//       .padding(1.5);

//   d3.csv("data/top_count_stations.csv", function(d) {
//     d.value = +d["bicicletar"];
//     d.Call_Type = d["neighborhood"]
//     return d;
//   }, function(error, data) {
//     if (error) throw error;

//     var color = d3.scaleOrdinal()
//     .domain(data.map(function(d){ return d.Call_Type;}))
//     .range(['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99',
//     '#e31a1c','#fdbf6f','#ff7f00','#cab2d6']);
    
//     var root = d3.hierarchy({children: data})
//         .sum(function(d) { return d.value; })

//     var node = svg.selectAll(".node")
//       .data(pack(root).leaves())
//       .enter().append("g")
//         .attr("class", "node")
//         .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
   
//     node.append("circle")
//         .attr("id", function(d) { return d.id; })
//         .attr("r", function(d) { return d.r; })
//         .style("fill", function(d) { return color(d.data.Call_Type); })
//         .on("mouseover", function(d) {      

//           d3.select(".tooltipleft")
//                     .style("visibility", "visible")
//                     .html(chordTip(d))
//                     .style("top", function () { return (d3.event.pageY - 20)+"px"})
//                     .style("left", function () { return (d3.event.pageX + 20)+"px";});
//     })                  
//       .on("mouseout", function(d) {     
//       d3.select(".tooltipleft").style("visibility", "hidden")
//     });

//      node.append("text")
//          .text(function(d) {
//            if (d.data.value > 0)
//             return d.data.Call_Type;
//            else
//             return "";
//         })
    
    
//   });
// });