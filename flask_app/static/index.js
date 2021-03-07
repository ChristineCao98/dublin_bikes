function initMap (){
  this.infowindow = new google.maps.InfoWindow();
  let myLatLng = {lat: 53.350140, lng: -6.266155};
  let map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: myLatLng,
  });

  //Display Cycle Routes on Map
  const bikeLayer = new google.maps.BicyclingLayer();
    bikeLayer.setMap(map);

  //Geolocation Feature on Map
  let geolocation = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          geolocation.setPosition(pos);
          geolocation.setContent("You are here!");
          geolocation.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, geolocation, map.getCenter());
        }
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, geolocation, map.getCenter());
    }
  });

  //Display Markers on Map
  axios.get('/api/stations/').then(response=>{
    var stations=response.data.data;
    stations.forEach(station=>{
    var marker=new google.maps.Marker({
    position:{lat:station.latitude,lng: station.longitude},
    map:map,
      icon:pinSymbol(getColor(station.available_bike))
  });
    marker.addListener("click",()=>{
    infowindow.setContent(station.number.toString());
    infowindow.open(map,marker);
    });
    });
  }).catch(error=>{
    console.log(error);
  });
}

function pinSymbol(color) {
    return {
        path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z M -2,-30 a 2,2 0 1,1 4,0 2,2 0 1,1 -4,0',
        fillColor: color,
        fillOpacity: 1,
        strokeColor: '#000',
        strokeWeight: 2,
        scale: 1,
   };
}
function getColor(num){
  if(num>20){
    return "#F00"
  }
  else{
    return "#0F0"
  }
}

function handleLocationError(browserHasGeolocation, geolocation, pos) {
  geolocation.setPosition(pos);
  geolocation.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  geolocation.open(map);
}
