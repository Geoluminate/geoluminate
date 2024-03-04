$(function () {
  map.fitWorld()
})

// const offCanvasRight = new bootstrap.Offcanvas($('#offcanvasright'))

var baseLayers = {
  "Dark Gray": L.esri.basemapLayer('DarkGray', {
    detectRetina: true
  }),
  "Imagery": L.esri.basemapLayer('Imagery', {
    detectRetina: true
  }),
  "Oceans": L.esri.basemapLayer('Oceans', {
    detectRetina: true
  }),
  "Topographic": L.esri.basemapLayer('Topographic', {
    detectRetina: true
  }),
  "Nat Geo": L.esri.basemapLayer('NationalGeographic', {
    detectRetina: true
  }),
}

var map = L.map('map', {
  layers: [baseLayers['Imagery']],
  minZoom: 3,
  maxZoom: 10,
  worldCopyJump: true,
  fullscreenControl: true,
  zoomControl: false,
})

L.control.layers(baseLayers).addTo(map)
L.control.zoom({
  position: 'topright'
}).addTo(map)
L.control.scale({
  position: 'bottomright'
}).addTo(map)

clusters = L.markerClusterGroup({
  chunkedLoading: true,
  disableClusteringAtZoom: 6,
  spiderfyOnMaxZoom: false,
})
map.addLayer(clusters)

$('#mainIndicator').toggle()

fetch($('#map').attr('url')).then((response) => response.json()).then((data) => {

  const test = data.results.map((item) => {
    return {
      type: 'Feature',
      geometry: item.geom,
      properties: {}
    }
  })

  console.log(test)
  var geojson = L.geoJSON(test, {
    pointToLayer: function (geoJsonPoint, latlng) {
      return L.circleMarker(latlng, {
        radius: 5,
        fill: true,
        fillOpacity: 0.75,
        fillColor: 'rgb(255,0,0,1)',
        color: 'rgb(200,0,0,1)', //stroke colour
        weight: 1, //stroke weight in pixels
      })
    },
    onEachFeature: onEachFeature,
  })
  clusters.addLayer(geojson)
  map.flyToBounds(geojson.getBounds())
  $('#mainIndicator').toggle()
})


function onEachFeature(feature, layer) {
  // attaches a click handler to each layer that will fetch the popup content
  layer.on({
    click: getPopupContent
  })
}

function getPopupContent(e) {
  // gets the popup content from the API


  // fetch($('#map').attr('url') + this.feature.id + '?format=html')
  fetch('/database/' + this.feature.id + '/?format=html')
    .then((response) => response.text())
    .then((html) => {
      offCanvasRight.toggle()
      $('#offcanvasright .offcanvas-body').html(html)
    })

  // $.get(`/api/v1/heat-flow/detail/${this.feature.id}`, function (content) {

  // })
}

// function getPopupContent(e) {
//   // gets the popup content from the API
//   var marker = this;
//   if (marker.getPopup() == undefined) {
//     $.get(`/api/v1/heat-flow/detail/${marker.feature.id}`, function (content) {
//       marker.bindPopup(content, {
//         maxHeight: 600,
//         maxWidth: 600
//       })
//       marker.openPopup()
//     })
//   }
// }



function get_url() {
  return $('#map').attr('url')
  // return $('#map').attr('url')
}

function updateMap() {

  url = '/api/geojson/site/?' + encodeURI($('#map-filter-form').serialize()) + encodeURI(reference)
  geojson.refresh(url)
  clusters.clearLayers()
  clusters.addLayer(geojson)
  map.flyToBounds(geojson.getBounds())
}

function filterSites(json) {
  var att = json.properties
  var lat_gt = $("input[name='latitude__gt']").val()
  return (att.latitude > lat_gt)
}
