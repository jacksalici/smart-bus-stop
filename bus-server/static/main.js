function displayMap(busLoc = undefined) {
  var map = L.map("map", {
    center: stationsList[0]["location"],
    zoom: 9,
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

  stationsList.forEach((station) => {
    var text = `Bus Stop "${station.name}" - <a href="/stop/${station.id}">View it</a>`;
    L.marker(station.location, {
      icon: busStopIcon,
      alt: "Station " + station.name,
    })
      .addTo(map)
      .bindPopup(text);
  });


  if (busLoc){
    var busIcon = L.icon({
      iconUrl:
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAADMUlEQVR4nO2Y30tTURzA9wfUS2/qzKAfZJOi7K2kUAQtihLUvOe2TBcpSVFWiueYzyVJ1EAoCsLRW1D4O03MHwVCKfjQQw+iRinmj1LDczb3jXO3e7erc9vd1rrJ/cKHu+2e+/1+Pzvn3DtmMhlhhBFhB6pbNp+vZcdEQq2IsFqEaSPC7CXCtBcRNoowGxMJneMgQpdEwoDjee39HLMxz1ja6722kefiOXluXsMUqyi5BVsFwipFTAdEQhfkhv4+dIHX5LXz62BLRM3n18E2hNlI/JpmGzHMe9EsIBL6UE4i4BU4e3sOTtz4BllXx+Dolc9w+PIwHLANQVrJe9hb3A+7rD2wQ+yCFIluMAsdkCS0Q5LQAWahE1LEt5Ai9sB2sQd2Wt/BnuJBsJQOwf5LHyG9bBSOVHyBzGvjkFs5BWeq5qWaigSmDzQLIMzG5QSpF3ohuagZkotaJMwSrT6ENoUkiXY/OvzohEQVbyARyXRBgkI37L74QRHg+yaSGXDLCTzNewTa7KnQat+nNN9qT4XJF6agtNgtmgUSULf/nnBHIOBbh/4CvPmWRxY/AUtIgWZ7WpQCDGImEK8llGAIEN8MZDb98vJzDQsBmFfjmFvDbAB+rGFGImZLyBBwxGEGUI3zJCLsa6CnoR5mQFQeamxSqHHmrl8ymE1u9DjXlQCRmAi65v8DAdj0AhO6E8DqJb5+ExParzSPnTl6ExBqnLmKBKZ9Ie9KehMwaQ1DoMmYATCWkOjdQDmPl+K+iXOezMduBvSAyRAgxgyAsYS0hP+3Zb3D4NlrF/R9WoWnr1zSe/lcVhmF47aViMgqo2HViHoTtw+ugn+0Dawq57LLKRwsWomI7HIaVo2oBRZ/q3LD4jIo5wqrGByKUKCgKrwaUQtMzbpVyb/PuFXJM0q0z0JGqe/bF8OoEZVAg8MFlHkS8+N9h0uVPK+SQroQfvN8bN5NtUBDiBpRCXAq7jKof+6UjoFuh4XVDE5fZ3AqBHwMHxsoR0WQGpoFUPX0P//5IMpUT2sXKLTVSxfqoflztnvaBQqQFYKhOWG86xVsAoH+jZLlC9bQ/wrovJ4RRmyW+ANCPg9GTyDq8wAAAABJRU5ErkJggg==",
    });

    L.marker(busLoc, {
      icon: busIcon,
    })
      .addTo(map)

  }
}
