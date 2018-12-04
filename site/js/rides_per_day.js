require(["https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js"], function (d3) {
    var formatDate1 = d3.time.format('%Y-%m-%d');
    var formatDate2 = d3.time.format('%d/%m/%Y');
    var formatP = d3.format('.1f');
    // var dias = {1: 'Seg', 2: 'Ter', 3: 'Quar', 4: 'Qui', 5: 'Sex', 6: 'Sab', 0: };
    var dias = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']

    function chordTip (d) {
            total = d.Men + d.Women + d.Others;
            pM = 100 * d.Men / total;
            pW = 100 * d.Women / total;
            pO = 100 * d.Others / total;
            return    `<strong>Data: ${formatDate2(d.dia)} (${dias[d.dia.getDay()]}) </strong><br /><div id='viagens_dia'></div><hr />
                               Total: ${total} <br />
                               Masculino: ${d.Men} (${formatP(pM)}%)<br />
                               Feminino: ${d.Women} (${formatP(pW)}%)<br />
                               Outros: ${d.Others} (${pO == 0? 0.0:formatP(pO)}%)`;

            // total = d.x + d.y;
            // pM = 100 * (d.x / total);
            // pF = 100 * (d.y / total);
            // if (pM > pF) {
            //     return   `<strong>Data: ${formatDate(d.date)}</strong><br />
            //                       Total: ${d.x + d.y} <br />
            //                       Masculino: ${d.x} (${formatP(pM)}%)<br />
            //                       Feminino: ${d.y} (${formatP(pF)}%)`;
            // } else {
            //     return   `<strong>Data: ${formatDate(d.date)}</strong><br />
            //                       Total: ${d.x + d.y} <br />
            //                       Feminino: ${d.y} (${formatP(pF)}%)<br />
            //                       Masculino: ${d.x} (${formatP(pM)}%)`;
            // }
        }
    // var title="Número de viagens ao longo dos anos";
    var title="";
    var units=" Viagens";
    var breaks=[500,1000,1500,2000,2500];
    // var colours=["#FFFFCC","#C7E9B4","#7FCDBB","#41B6C4","#2C7FB8","#253494"];
    // var colours=["#edf8fb","#ccece6","#99d8c9","#66c2a4","#2ca25f","#006d2c"];
    var colours=["#99d8c9","#66c2a4","#41ae76","#238b45","#006d2c","#00441b"]

    //general layout information
    var cellSize = 17;
    var xOffset=30;
    var yOffset=60;
    var calY=50;//offset of calendar in each group
    var calX=25;
    var width = 960;
    var height = 150;
    var parseDate = d3.time.format("%Y-%m-%d").parse;
    format = d3.time.format("%Y-%m-%dd");
    toolDate = d3.time.format("%Y-%m-%d");
    
    d3.csv("data/rides_per_sex.csv", function(error, data) {
        
        //set up an array of all the dates in the data which we need to work out the range of the data
        var dates = new Array();
        var values = new Array();
        var median = d3.format(".2f");
        //parse the data
        data.forEach(function(d)    {
                dates.push(parseDate(d.dia));
                d.dia=parseDate(d.dia);
                d.Men=parseInt(d.M_0);
                d.Women=parseInt(d.F_0);
                d.Others=parseInt(d.O_0);
                d.year=d.dia.getFullYear();//extract the year from the data
        });
        
        var yearlyData = d3.nest()
            .key(function(d){return d.year;})
            .entries(data);
        
        var svg = d3.selectAll("#calendar_viagens").append("svg")
            .attr("width","100%")
            .attr("viewBox","0 0 "+(xOffset+width)+" 870")
            
        //title
        svg.append("text")
        .attr("x",xOffset)
        .attr("y",20)
        .text(title);        

        
        //create an SVG group for each year
        var cals = svg.selectAll("g")
            .data(yearlyData)
            .enter()
            .append("g")
            .attr("id",function(d){
                return d.key;
            })
            .attr("transform",function(d,i){
                return "translate(0,"+(yOffset+(i*(height+calY)))+")";  
            })
        
        var labels = cals.append("text")
            .attr("class","yearLabel")
            .attr("x",xOffset)
            .attr("y",15)
            .text(function(d){return d.key});
        
        //create a daily rectangle for each year
        var rects = cals.append("g")
            .attr("id","alldays")
            .selectAll(".day")
            .data(function(d) { return d3.time.days(new Date(parseInt(d.key), 0, 1), new Date(parseInt(d.key) + 1, 0, 1)); })
            .enter().append("rect")
            .attr("id",function(d) {
                return "_"+format(d);
            })
            .attr("class", "day")
            .attr("width", cellSize)
            .attr("height", cellSize)
            .attr("x", function(d) {
                return xOffset+calX+(d3.time.weekOfYear(d) * cellSize);
            })
            .attr("y", function(d) { return calY+(d.getDay() * cellSize); })
            .datum(format);
        
        //create day labels
        // var days = ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'];
        var days = ['D','S','T','Q','Q','S','S'];
        var dayLabels=cals.append("g").attr("id","dayLabels")
        days.forEach(function(d,i)    {
            dayLabels.append("text")
            .attr("class","dayLabel")
            .attr("x","3.5em")
            .attr("y",function(d) { return calY+(i * cellSize); })
            .attr("dy","1em")
            .text(d);
        })
        
        //let's draw the data on
        var dataRects = cals.append("g")
            .attr("id","dataDays")
            .selectAll(".dataday")
            .data(function(d){
                return d.values;   
            })
            .enter()
            .append("rect")
            .attr("id",function(d) {
                return format(d.dia)+":"+d.Men;
            })
            .attr("stroke","#fff")
            .attr("width",cellSize)
            .attr("height",cellSize)
            .attr("x", function(d){return xOffset+calX+(d3.time.weekOfYear(d.dia) * cellSize);})
            .attr("y", function(d) { return calY+(d.dia.getDay() * cellSize); })
            .attr("fill", function(d) {
        sum = (d.Men + d.Women + d.Others);
                if (sum<=0) {
                    return "#FFFFFF";
                }
                for (i=0;i<breaks.length+1;i++){
                    if (sum<=breaks[i]){
                        return colours[i];
                    }
                }
                if (sum>breaks[4]){
                    return colours[breaks.length]   
                }
            })
        dataRects.on("mouseover", function (d) {
                    d3.select(this)
                      .attr("stroke", "#fff")
                      .attr("stroke-width", 3);
                    d3.select(".tooltipleft")
                      .style("visibility", "visible")
                      .html(chordTip(d))
                      .style("top", function () { return (d3.event.pageY - 150)+"px"})
                      .style("left", function () { return (d3.event.pageX - 150)+"px";});

                    plot_rides(formatDate1(d.dia), "#viagens_dia")
                 })
                 .on("mouseout", function (d) {
                    d3.select(this)
                      .attr("stroke", "#FFF")
                      .attr("stroke-width", 1);
                    d3.select(".tooltipleft").style("visibility", "hidden");
                 })


        //append a title element to give basic mouseover info
        // dataRects.append("title")
            // .text(function(d) { return toolDate(d.dia)+"\nSoma: "+(d.Men + d.Women + d.Others)+units+"\nHomens: "+d.Men+units+"\nMulheres: "+d.Women+units+"\nOutros: "+d.Others+units;});
        
        // dataRects.on("mouseover", function(d){
        //     d3.select(this)
        //       .attr("stroke", "#FFF")
        //       .attr("stroke-width", 2);
        // });

        //add montly outlines for calendar
        cals.append("g")
        .attr("id","monthOutlines")
        .selectAll(".month")
        .data(function(d) { 
            return d3.time.months(new Date(parseInt(d.key), 0, 1),
                                  new Date(parseInt(d.key) + 1, 0, 1)); 
        })
        .enter().append("path")
        .attr("class", "month")
        .attr("transform","translate("+(xOffset+calX)+","+calY+")")
        .attr("d", monthPath);
        
        //retreive the bounding boxes of the outlines
        var BB = new Array();
        var mp = document.getElementById("monthOutlines").childNodes;
        for (var i=0;i<mp.length;i++){
            BB.push(mp[i].getBBox());
        }
        
        var monthX = new Array();
        BB.forEach(function(d,i){
            boxCentre = d.width/2;
            monthX.push(xOffset+calX+d.x+boxCentre);
        })

        //create centred month labels around the bounding box of each month path
        //create day labels
        // var months = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'];
        // var months = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
        var months = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
        var monthLabels=cals.append("g").attr("id","monthLabels")
        months.forEach(function(d,i)    {
            monthLabels.append("text")
            .attr("class","monthLabel")
            .attr("x",monthX[i])
            .attr("y",calY/1.2)
            .text(d);
        })
        
         //create key
        var key = svg.append("g")
            .attr("id","key")
            .attr("class","key")
            .attr("transform",function(d){
                return "translate("+xOffset+","+(yOffset-(cellSize*1.5))+")";
            });
        
        key.selectAll("rect")
            .data(colours)
            .enter()
            .append("rect")
            .attr("width",cellSize)
            .attr("height",cellSize)
            .attr("x",function(d,i){
                return i*130;
            })
            .attr("fill",function(d){
                return d;
            });
        
        key.selectAll("text")
            .data(colours)
            .enter()
            .append("text")
            .attr("x",function(d,i){
                return cellSize+5+(i*130);
            })
            .attr("y","1em")
            .text(function(d,i){
                if (i<colours.length-1){
                    return "até "+breaks[i];
                }   else    {
                    return "acima de "+breaks[i-1];   
                }
            });
        
    });//end data load
    
    //pure Bostock - compute and return monthly path data for any year
    function monthPath(t0) {
      var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
          d0 = t0.getDay(), w0 = d3.time.weekOfYear(t0),
          d1 = t1.getDay(), w1 = d3.time.weekOfYear(t1);
      return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
          + "H" + w0 * cellSize + "V" + 7 * cellSize
          + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
          + "H" + (w1 + 1) * cellSize + "V" + 0
          + "H" + (w0 + 1) * cellSize + "Z";
    }
});