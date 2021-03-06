require(["https://cdnjs.cloudflare.com/ajax/libs/d3/5.7.0/d3.min.js"], function (d3) {
    
 var blueIcon = new L.Icon({
  iconUrl: 'images/img/marker-icon-2x-blue.png',
  shadowUrl: 'images/img/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var redIcon = new L.Icon({
  iconUrl: 'images/img/marker-icon-2x-red.png',
  shadowUrl: 'images/img/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var greenIcon = new L.Icon({
  iconUrl: 'images/img/marker-icon-2x-green.png',
  shadowUrl: 'images/img/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var orangeIcon = new L.Icon({
  iconUrl: 'images/img/marker-icon-2x-orange.png',
  shadowUrl: 'images/img/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var yellowIcon = new L.Icon({
  iconUrl: 'images/img/marker-icon-2x-yellow.png',
  shadowUrl: 'images/img/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var violetIcon = new L.Icon({
  iconUrl: 'images/img/marker-icon-2x-violet.png',
  shadowUrl: 'images/img/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var greyIcon = new L.Icon({
  iconUrl: 'images/img/marker-icon-2x-grey.png',
  shadowUrl: 'images/img/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var blackIcon = new L.Icon({
  iconUrl: 'images/img/marker-icon-2x-black.png',
  shadowUrl: 'images/img/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});


var translateColors = [blackIcon, blueIcon, redIcon, greenIcon, violetIcon, greyIcon]
var translateColors2 = ['#3c3c3c', '#4698d0', '#cb293c', '#24ac21', '#9a27ca', '#787878']





    function toTitleCase(str) {
      return str.replace(/\w\S*/g, function(txt){
          return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    }

    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00'];
    let colorScale = d3.scaleOrdinal().domain([1,2,3,4,5]).range(colors);

    

    // escala de cores
    

    let map = L.map('install_station',{zoomControl: false}).setView([-3.742616,-38.5035877], 13);
    // L.tileLayer("https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",{ attribution: 'aasd', maxZoom: 11.5, minZoom: 11.5, opacity: 0}).addTo(map2);
    L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors', maxZoom: 15, minZoom: 13
    }).addTo(map);
    map.touchZoom.disable();
    map.doubleClickZoom.disable();
    // map.scrollWheelZoom.disable();
    var bounds = L.latLngBounds([[-3.68,-38.585713], [-3.806353,-38.43156]]);
    map.setMaxBounds(bounds);
    stations = []
    d3.csv("data/stations_with_new_neighborhood.csv").then(function (data) {
        data.forEach(function(d) {
            d.media_viagens = 1450;
            stations.push(d);
            // var circle = L.circle([d.lat, d.lon], {
            //     color: colorScale(d.etapa),
            //     fillColor: colorScale(d.etapa),
            //     fillOpacity: 0.5,
            //     opacity: 1,
            //     radius: 80,
            // })
            var circle = L.marker([d.lat, d.lon], {
              icon: translateColors[d.etapa],
              number: 10
            })
            circle.bindPopup(`<h5><strong>Estação ${d.id}: ${d.nome_estacao}</strong></h5>
                  Localizada no bairro <strong>${toTitleCase(d.bairro)}</strong>, a estação <strong>${d.id}</strong> participa do programa <strong>${d.programa}</strong> e foi instalada na etapa <strong>${d.etapa}</strong>.`);
            circle.addTo(map);
            // console.log(circle);
        });
    });
    


    let legend = L.control({position: 'topright'});

    legend.onAdd = function (map) {

      let div = L.DomUtil.create('div', 'info legend'),
        labels = [],
              n = colors.length,
        from, to;
      for (let i = 0; i < n; i++) {
         let c = translateColors2[i];
        //       let fromto = quantize.invertExtent(c);
        str = `<i style="background:${translateColors2[i+1]}"></i> Etapa ${i+1}`;
        labels.push(str)
        //   d3.format("d")(fromto[0]) + (d3.format("d")(fromto[1]) ? '&ndash;' + d3.format("d")(fromto[1]) : '+'));
      }
      labels.push(`<i style="background:${translateColors2[0]}"></i> Minibicicletar`)
      div.innerHTML = labels.join('<br>');
      return div;
    };
    legend.addTo(map);
    

    // let pointsLayer = L.layerGroup().addTo(map);

    // pointsLayer.addLayer(c);



    // Criação do Mapa


//     L.tileLayer("https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
//     { attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
//     maxZoom: 13, minZoom: 12}).addTo(map);
    
// map.dragging.disable();
// // `<strong>Estação ${d.id}: ${d.nome_estacao}</strong><br />
// //                       - Bairro: ${toTitleCase(d.bairro)}<br />
// //                       - Programa: ${d.programa}<br />
// //                       - Implantação: etapa ${d.etapa}<br />
// //                       - Média diária: 150<br />`

//     // Criação dos markers e layer

//     var markers = d3.map();
//     var markerLayer = L.layerGroup();

//     //Facts e Dimensions

//     let facts = crossfilter(data);
//     var etapasDimension = facts.dimension(function(d) {return d.etapa});
    
//     let colorScale = d3.scaleOrdinal()
//                           .domain([1,2,3,4,5])
//                           .range(['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99']);

//     let pointsLayer = L.layerGroup().addTo(map);

//     for (let d of data) {
//         let c = L.circle([d.lat, d.lon], 100, { 
//                 color: colorScale(d.etapa),
//                 weight: 2,
//                 fillColor: colorScale(d.etapa),
//                 fillOpacity: 0.5            
//             });
//         c.bindPopup(

//                   `<h6>Estação ${d.id}: ${d.nome_estacao}</h6>
//                   Localizada no bairro <strong>${toTitleCase(d.bairro)}</strong>, a estação <strong>${d.id}</strong> participa do programa <strong>${d.programa}</strong> e foi instalada na etapa <strong>${d.etapa}</strong>.
//                   Deste de sua instalação, esta estação tem uma média de <strong>1045</strong> viagens diárias.`);
//         pointsLayer.addLayer(c);
//     }   

//     facts.onChange(() =>{   
//         var e = +document.getElementById("sliderEtapas").value;             
        
//         let colorScale2 = d3.scaleOrdinal()
//                           .domain([false,true])
//                           .range(["#66c2a4","#005824"]);  

//         pointsLayer.clearLayers();
//         for (let d of facts.allFiltered()) {                                                
//             let c = L.circle([d.lat, d.lon], 100, { 
//                 color: colorScale2(e==d.etapa),
//                 weight: 2,
//                 fillColor: colorScale2(e==d.etapa),
//                 fillOpacity: 0.5            
//             });
//         console.log(d);
//             c.bindPopup(`<strong>Estação ${d.nome_estacao}</strong><br />
//                      Implantação: etapa ${d.etapa}<br />`);
//             pointsLayer.addLayer(c);                
//         }
//     }); 

//     window.updateMarkers = function(){
//         var e = +document.getElementById("sliderEtapas").value;             
//         etapasDimension.filter([1,e+1]);            
//     }  

// dc.renderAll();
});