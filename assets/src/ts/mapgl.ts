import { Map } from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"


const colorCycle = [
  "#1f77b4",
  "#ff7f0e",
  "#2ca02c",
  "#d62728",
  "#9467bd",
  "#8c564b",
  "#e377c2",
  "#7f7f7f",
  "#bcbd22",
  "#17becf"
];


function basicMap(container: string, sourceList: any) {

  const map = new Map({
    container: container,
    style: 'https://demotiles.maplibre.org/style.json',
    center: [0, 0],
    zoom: 1
  });

  map.on('load', function () {
    // Add sources and layers here
    Object.entries(sourceList).forEach(([key, geojson_str], index) => {

        map.addSource(key, {
          type: 'geojson',
          data: JSON.parse(geojson_str as string)
        })

        map.addLayer({
          'id': key,
          'type': 'circle',
          'source': key,
          'layout': {},
          'paint': {
            'circle-radius': 4,
            'circle-color': colorCycle[index % colorCycle.length],
          },
        })

      })


  })


  return map;
}


(window as any).basicMap = basicMap;
