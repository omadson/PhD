// let blues = d3.schemeBlues[8];
// &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>
let map = L.map('map_estacoes', {zoomControl: false}).setView([-3.792614,-38.515877], 11.5);
L.tileLayer("https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
{ attribution: '',
maxZoom: 11.5, minZoom: 11.5, opacity: 0}).addTo(map);

  map.dragging.disable();
  map.touchZoom.disable();
  map.doubleClickZoom.disable();
  map.scrollWheelZoom.disable();
// control that shows state info on hover
let info = L.control({position: 'bottomleft'});

info.onAdd = function (map) {
  this._div = L.DomUtil.create('div', 'info');
  this.update();
  return this._div;
};

info.update = function (feat) {
          //console.log(feat);
    this._div.innerHTML = (feat ?
      '<b>' + feat.properties.NOME + '</b><br />Bicicletar: ' + bicicletarByName.get(feat.properties.NOME) + '<br />Mini bicicletar: ' + minibicicletarByName.get(feat.properties.NOME) : 'Passe o mouse sobre um bairro');
};

info.addTo(map);

// get color depending on number of cases
// let quantize = d3.scaleQuantize()
//    .domain([0, 200])
//    .range(blues);

  let blues = d3.quantize(d3.interpolateGreens, 6);
  let quantize = d3.scaleQuantile().domain([1,2,3,4,10,13]).range(blues);

function style(feature) {
   stationsCount = bicicletarByName.get(feature.properties.NOME) + minibicicletarByName.get(feature.properties.NOME);
   return {
        weight: 1,
        opacity: 1,
        color: 'black',
        fillOpacity: 1,
        fillColor: stationsCount != NaN?quantize(stationsCount):'#000'
      };
}
function highlightFeature(e) {
  let layer = e.target;
      //console.log(e.target)

  layer.setStyle({
        weight: 3,
        color: '#000',
        dashArray: '',
        fillOpacity: 1
  });

  if (!L.Browser.ie && !L.Browser.opera) {
    layer.bringToFront();
  }

  info.update(layer.feature);
}
let geojson;

function resetHighlight(e) {
  geojson.resetStyle(e.target);
  info.update();
}

function zoomToFeature(e) {
  map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
  layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        // click: zoomToFeature
      });
}
  let bicicletarByName = d3.map();

let minibicicletarByName = d3.map();

  let promises = [
    d3.csv("data/count_stations.csv"),
]


Promise.all(promises).then(ready);

function ready([count_stations]) {
  //format data
      count_stations.forEach(function(d) {
          bicicletarByName.set(d.neighborhood,+d.bicicletar);
          minibicicletarByName.set(d.neighborhood,+d.minibicicletar);
      });
  
  //bairrosData is defined in file bairros.js       
  geojson = L.geoJson(bairrosData, {
      style: style,
      onEachFeature: onEachFeature
  }).addTo(map);
}

let legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

  let div = L.DomUtil.create('div', 'info legend'),
    labels = [],
          n = blues.length,
    from, to;

  for (let i = 0; i < n; i++) {
    let c = blues[i];
          let fromto = quantize.invertExtent(c);
    labels.push(
      '<i style="background:' + blues[i] + '"></i> ' +
      d3.format("d")(fromto[0]) + (d3.format("d")(fromto[1]) ? '&ndash;' + d3.format("d")(fromto[1]) : '+'));
  }

  div.innerHTML = labels.join('<br>');
  return div;
};

legend.addTo(map);
document.getElementsByClassName( 'leaflet-control-attribution' )[0].style.display = 'none';