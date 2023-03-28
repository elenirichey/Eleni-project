const userZip = document.querySelector('#zipcode').innerText;
console.log(userZip)

const PLACEIDS = new Set();
const ALLPARKS = [];//or make it a set?
const keywords = ['playground', 'park', 'swings', 'slide'];

var map;
var service;
var infowindow;

    

function initMap() {

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: userZip }, (results, status) => {
      if (status === 'OK') {
       
        const userLocation = results[0].geometry.location;
        const userLat = results[0].geometry.location.lat();
        const userLng = results[0].geometry.location.lng();
        console.log(userLat)
        console.log(userLng)
        
        
    const map = new google.maps.Map(document.querySelector('#map'), {
        center: {lat: userLat, lng: userLng},
        zoom: 11,
        });

    const locale = {'loc': userLocation, 'zipcode': userZip};
    const parkInfo = new google.maps.InfoWindow();

    // for (const keyword of keywords) {
    var request = {
    location: userLocation,
    radius: '5000',
    query: "park+playground"
  };

  service = new google.maps.places.PlacesService(map);
  service.textSearch(request, callback);


function callback(results, status) {
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      var place = results[i];
      createMarker(results[i]);
     } }
  }}
}
// }
)
}