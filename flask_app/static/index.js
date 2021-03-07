'use strict';//to enable the use of let

var markerMap=new Map();
function initMap (){
  this.infowindow = new google.maps.InfoWindow();
  let myLatLng = {lat: 53.350140, lng: -6.266155};
  let map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: myLatLng,
  });
  axios.get('/api/stations/').then(response=>{
    var stations=response.data.data;
    stations.forEach(station=>{
    var scale=getSize(station.available_bike);
    var color=getColor(station.available_bike);
    var marker=new google.maps.Marker({
    position:{lat:station.latitude,lng: station.longitude},
    map:map,
    // icon:pinSymbol(getColor(station.available_bike))
        icon:`https://chart.apis.google.com/chart?chst=d_map_spin&chld=${scale}|0|${color}|11|_|${station.available_bike}`
  });
    markerMap.set(station.number,marker);
    marker.addListener("click",()=>{
    infowindow.setContent(station.number.toString());
    infowindow.open(map,marker);
    });
    });
  }).catch(error=>{
    console.log(error);
  });
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