const userZip = document.querySelector('#zipcode').value

function initMap() {

  const basicMap = new google.maps.Map(document.querySelector('#map'), {
    zoom: 11,
  });

  const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: userZip }, (results, status) => {
      if (status === 'OK') {
        // Get the coordinates of the user's location
        const userLocation = results[0].geometry.location;
  
        // Create a marker
        new google.maps.Marker({
          position: userLocation,
          map,
        });
  
        map.setCenter(userLocation);
        map.setZoom(18);
      } else {
        alert(`Geocode was unsuccessful for the following reason: ${status}`);
      }
    });
  }

  // const geocoder = new google.maps.Geocoder();
  // geocoder.geocode( { 'address': userZip}, function (result, status) {
  //   cur_lng = result[0].geometry.location.lng();
  //   cur_lat = result[0].geometry.location.lat();

  //   const location = new google.maps.LatLng(cur_lat, cur_lng);
  // });
  
  // map.setCenter(location);

// }









//   const geocoder = new google.maps.Geocoder();
//   geocoder.geocode({ address: userZip }, (results, status) => {
//     if (status === 'OK') {
//       // Get the coordinates of the user's location
//       const userLocation = results[0].geometry.location;

//       // Create a marker
//       new google.maps.Marker({
//         position: userLocation,
//         map,
//       });

//       map.setCenter(userLocation);
//       map.setZoom(18);
//     } else {
//       alert(`Geocode was unsuccessful for the following reason: ${status}`);
//     }
//   });
// }




  // const basicMap = new google.maps.Map(document.querySelector('#map'), {
  // center: userLocation,
  // zoom: 11,
  // });



// }
// });
// }









// // const userZip = document.querySelector('#zipcode').value

// // function initMap() {

// //     const geocoder = new google.maps.Geocoder();
// //             geocoder.geocode({ address: userZip }, (results, status) => {
// //         if (status === 'OK') {
// //         // Get the coordinates of the user's location
// //         const userLocation = results[0].geometry.location;

// //     const basicMap = new google.maps.Map(document.querySelector('#map'), {
// //                 center: userLocation,
// //                 zoom: 11,
// //               });
    
// //     const plotParks = (parks) => {
// //                 // array of parks, use marker to plot on map and fit bounds to center
// //             }
// //             // PlacesService(mapTarget.current)
// //     const service = new window.google.maps.places.PlacesService(basicMap);
            
// //             // radius in meters so I added mile to radius, seems correct, formula pulled from SO ha
// //     const radiusInMeters = (Math.round(10000*(radiusMiles*5280 / 3.281))/10000);
            
// //     // location: mapTarget.current.getCenter()
// //     service.nearbySearch(
// //         {location: basicMap.getCenter(), radius: radiusInMeters, type: ['playground']},
// //         (results, status, pagination) => {
// //             if (status !== 'OK' || !results.length) {
// //                         alert('No parks found near you, try increasing your radius or try a new address');
// //         } else {
// //             plotParks(results);
// //                     }
// //         });
   

// // }})}

// function getLatLngByZipcode(userZip) 
// {

// geocoder.geocode({ 'address': address }, function (results, status) {
//   if (status == google.maps.GeocoderStatus.OK) {
//       var latitude = results[0].geometry.location.lat();
//       var longitude = results[0].geometry.location.lng();
//       alert("Latitude: " + latitude + "\nLongitude: " + longitude);
//   } else {
//       alert("Request failed.")
//   }
// });
// return [latitude, longitude];

// const userZip = document.querySelector('#zipcode').value
// let map, infoWindow;

// function initMap() {


//   const geocoder = new google.maps.Geocoder();
// //         geocoder.geocode({ address: userAddress }, (results, status) => {
// //           if (status === 'OK') {
// //             // Get the coordinates of the user's location
// //             const userLocation = results[0].geometry.location;
//   map = new google.maps.Map(document.getElementById("map"), {
//     center: { userZip },
//     zoom: 6,
//   });
//   infoWindow = new google.maps.InfoWindow();

//   const locationButton = document.createElement("button");

//   locationButton.textContent = "Pan to Current Location";
//   locationButton.classList.add("custom-map-control-button");
//   map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
//   locationButton.addEventListener("click", () => {
//     // Try HTML5 geolocation.
//     if (navigator.geolocation) {
//       navigator.geolocation.getCurrentPosition(
//         (position) => {
//           const pos = {
//             lat: position.coords.latitude,
//             lng: position.coords.longitude,
//           };

//           infoWindow.setPosition(pos);
//           infoWindow.setContent("Location found.");
//           infoWindow.open(map);
//           map.setCenter(pos);
//         },
//         () => {
//           handleLocationError(true, infoWindow, map.getCenter());
//         }
//       );
//     } else {
//       // Browser doesn't support Geolocation
//       handleLocationError(false, infoWindow, map.getCenter());
//     }
//   });
// }

// function handleLocationError(browserHasGeolocation, infoWindow, pos) {
//   infoWindow.setPosition(pos);
//   infoWindow.setContent(
//     browserHasGeolocation
//       ? "Error: The Geolocation service failed."
//       : "Error: Your browser doesn't support geolocation."
//   );
//   infoWindow.open(map);
// }

// window.initMap = initMap;







// // 'use strict';

// // function initMap() {
// //     document.querySelector('#geocode-address').addEventListener('click', () => {
// //         const userAddress = prompt('Enter a location');
    
// //         const geocoder = new google.maps.Geocoder();
// //         geocoder.geocode({ address: userAddress }, (results, status) => {
// //           if (status === 'OK') {
// //             // Get the coordinates of the user's location
// //             const userLocation = results[0].geometry.location;
    
// //             // Create a marker
// //             new google.maps.Marker({
// //               position: userLocation,
// //               map,
// //             })}});
        
// //         })}
// //         window.initMap = initMap;


    
        


// // const userZip = document.querySelector('#zipcode').value

// // function initMap() {

// //     const geocoder = new google.maps.Geocoder();
// //             geocoder.geocode({ address: userZip }, (results, status) => {
// //         if (status === 'OK') {
// //         // Get the coordinates of the user's location
// //         const userLocation = results[0].geometry.location;

// //     const basicMap = new google.maps.Map(document.querySelector('#map'), {
// //                 center: userLocation,
// //                 zoom: 11,
// //               });
    
// //     const plotParks = (parks) => {
// //                 // array of parks, use marker to plot on map and fit bounds to center
// //             }
// //             // PlacesService(mapTarget.current)
// //     const service = new window.google.maps.places.PlacesService(basicMap);
            
// //             // radius in meters so I added mile to radius, seems correct, formula pulled from SO ha
// //     const radiusInMeters = (Math.round(10000*(radiusMiles*5280 / 3.281))/10000);
            
// //     // location: mapTarget.current.getCenter()
// //     service.nearbySearch(
// //         {location: basicMap.getCenter(), radius: radiusInMeters, type: ['playground']},
// //         (results, status, pagination) => {
// //             if (status !== 'OK' || !results.length) {
// //                         alert('No parks found near you, try increasing your radius or try a new address');
// //         } else {
// //             plotParks(results);
// //                     }
// //         });
   

// // }})}



// // function initMap() {
// //     // Code that works with Google Maps here
// //     document.querySelector('#playground-search').addEventListener('click', () => {
// //         const userZip = prompt ('enter a zipcode');

// //     //     const plotParks = (parks) => {
// //     //     // array of parks, use marker to plot on map and fit bounds to center
// //       // }
// //       const basicMap = new google.maps.Map(document.querySelector('#map'), {
// //         center: userZip,
// //         zoom: 11,
// //       });

// //         const geocoder = new google.maps.Geocoder();
// //         geocoder.geocode({ address: userZip }, (results, status) => {
// //       if (status === 'OK') {
// //         // Get the coordinates of the user's location
// //         const userLocation = results[0].geometry.location;

// //         // Create a marker
// //         new google.maps.Marker({
// //           position: userLocation,
// //           map,
// //         });

// //         // Zoom in on the geolocated location
// //         map.setCenter(userLocation);
// //         map.setZoom(18);
// //       } else {
// //         alert(`Geocode was unsuccessful for the following reason: ${status}`);
// //       }
// //     });
// //   });
// //     const service = new window.google.maps.places.PlacesService(userLocation)
// //     // const service = new window.google.maps.places.PlacesService(mapTarget.current);
    
// //     // radius in meters so I added mile to radius, seems correct, formula pulled from SO ha
// //     const radiusInMeters = (Math.round(10000*(radiusMiles*5280 / 3.281))/10000);
// //     // const plotParks = (parks) => {
// //     //     // array of parks, use marker to plot on map and fit bounds to center
// //     // }
// //     service.nearbySearch(
// //         {location: userLocation.getCenter(), radius: radiusInMeters, type: ['playground']},
// //         (results, status, pagination) => {
// //             if (status !== 'OK' || !results.length) {
// //                 alert('No parks found near you, try increasing your radius or try a new address');
// //         } else {
// //             plotParks(results);
// //                     }
// //         });
// //   }