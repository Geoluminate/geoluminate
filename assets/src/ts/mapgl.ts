import { Map } from "maplibre-gl"

// listen for htmx settle event
document.addEventListener("htmx:afterSettle", function (event) {
  // get the map element
  var mapElement = (event.target as Element).querySelector("#map")
  if (mapElement) {
    // create the map
    var map = new Map({
      container: "map", // container id
      style: 'https://demotiles.maplibre.org/style.json', // style URL
      center: [0, 0], // starting position [lng, lat]
      zoom: 1 // starting zoom
    })
  }
})


