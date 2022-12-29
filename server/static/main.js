function displayMap() {
  var map = L.map("map", {
    center: stationsList[Object.keys(stationsList)[0]]["coord"],
    zoom: 12,
  });

  const key = "zeNHm3ioxQhNUuX6E3yj";

  map.attributionControl.setPrefix("");

  L.tileLayer(
    `https://api.maptiler.com/maps/basic-v2-light/{z}/{x}/{y}.png?key=${key}`,
    {
      //style URL
      tileSize: 512,
      zoomOffset: -1,
      minZoom: 1,
      attribution:
        '&copy; <a href="https://www.maptiler.com/copyright/" target="_blank"> MapTiler</a> and <a href="https://www.openstreetmap.org/copyright" target="_blank"> OpenStreetMap </a>',
      crossOrigin: true,
      //detectRetina:true
    }
  ).addTo(map);

  //https://img.icons8.com/color/48/null/bus.png
  var busStopIcon = L.icon({
    iconUrl:
      "https://img.icons8.com/external-flaticons-flat-flat-icons/64/000000/external-bus-stop-traditional-marketing-flaticons-flat-flat-icons.png",
  });

  Object.keys(stationsList).forEach((station) => {
    var text = `Bus Stop "${stationsList[station].name}" - <a href="/${station}">View it</a>`;
    L.marker(stationsList[station].coord, {
      icon: busStopIcon,
      alt: "Station " + stationsList[station].name,
    })
      .addTo(map)
      .bindPopup(text);
  });
}
