'use strict';//to enable the use of let

var markerMap=new Map();
var stationInfo=new Map();
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
  locationButton.type="button";
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
    var scale=getSize(station.available_bike);
    var color=getColor(station.available_bike);
    var marker=new google.maps.Marker({
    position:{lat:station.latitude,lng: station.longitude},
    map:map,
    icon:`https://chart.apis.google.com/chart?chst=d_map_spin&chld=${scale}|0|${color}|11|_|${station.available_bike}`
  });
    markerMap.set(station.number,marker);
    stationInfo.set(station.number,station);
    marker.addListener("click",()=>{
    infowindow.setContent(station.number.toString());
    infowindow.open(map,marker);
    });
    });
  }).catch(error=>{
    console.log(error);
  });
}
function displayMarker(sign){
    markerMap.forEach(function(value, key){
        var station=stationInfo.get(key);
        var num=sign==0?station.available_bike:station.available_bike_stand;
        var scale=getSize(num);
        var color=getColor(num);
        value.setIcon(`https://chart.apis.google.com/chart?chst=d_map_spin&chld=${scale}|0|${color}|11|_|${num}`)
    })
}
function getSize(num){
    if(num>20){
    return 0.75
  }
  else{
    return 0.5
  }
}
function getColor(num){
  if(num>20){
    return "F00000"
  }
  else{
    return "00FF00"
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
