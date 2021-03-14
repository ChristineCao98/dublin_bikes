'use strict';//to enable the use of let
google.charts.load('current', {'packages':['corechart']});
google.charts.load('current', {'packages':['bar']});
var markerMap=new Map();
var stationInfo=new Map();
var infowindow;
var map;
var weekday=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
function initMap (){

  infowindow = new google.maps.InfoWindow();
  let myLatLng = {lat: 53.350140, lng: -6.266155};
  map = new google.maps.Map(document.getElementById("map"), {
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
    marker.addListener("click",()=>clickEvent(station.number));
    });
  }).catch(error=>{
    console.log(error);
  });
}
function clickEvent(id){
  showStatic(id);
  showHourly(id);
  showDaily(id);
}
function showStatic(id){
  var station=stationInfo.get(id);
  var marker=markerMap.get(id);
  var content=`
  <h6>Basic information</h6>
  <ul>
  <li>Station No.${station.number}</li>
  <li>Full address: ${station.address}</li>
  <li>Available bikes: ${station.available_bike}</li>
  <li>Free stands: ${station.available_bike_stand}</li>
  <li>Total capacity: ${station.bike_stand}</li>
</ul>
  `;
  infowindow.setContent(content);
  infowindow.open(map,marker);
}
function showHourly(id){
  axios.get('/api/hour/'+id).then(response=>{
    var data = new google.visualization.DataTable();
      data.addColumn('string', 'Hour of Day');
      data.addColumn('number','average number');
      response.data.forEach(hourlydata=>{
        data.addRow([hourlydata.hour.toString(),hourlydata.available_bike]);
      });
      var options = {
        title: 'Hourly availability data',
        width:1100,
        hAxis: {
          title: 'Hour of day',
          showTextEvery: 1
        },
        vAxis: {
          title: 'average number'
        }
      };
      var materialChart = new google.charts.Bar(document.getElementById('hourly-chart'));
      materialChart.draw(data, options);
  }).catch(error=>{
    console.log(error);
  });
}
function showDaily(id){
  axios.get('/api/day/'+id).then(response=>{
    var data = new google.visualization.DataTable();
      data.addColumn('string', 'Day of Week');
      data.addColumn('number','average number');
      response.data.forEach(dailydata=>{
        data.addRow([weekday[dailydata.day],dailydata.available_bike]);
      });
      var options = {
        title: 'Daily availability data',
        width:1000,
        hAxis: {
          title: 'day of week',
          showTextEvery: 1
        },
        vAxis: {
          title: 'average number'
        }
      };
      var materialChart = new google.charts.Bar(document.getElementById('daily-chart'));
      materialChart.draw(data, options);
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
