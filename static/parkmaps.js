'use strict';

function initMap() {
    const map = new google.maps.Map(document.querySelector('#map'), {
      center: {
        lat: 37.601773,
        lng: -122.20287,
      },
      zoom: 11,
    });
}  

// const userZip = document.querySelector('#zipcode').value

// function initMap() {

//     const geocoder = new google.maps.Geocoder();
//             geocoder.geocode({ address: userZip }, (results, status) => {
//         if (status === 'OK') {
//         // Get the coordinates of the user's location
//         const userLocation = results[0].geometry.location;

//     const basicMap = new google.maps.Map(document.querySelector('#map'), {
//                 center: userLocation,
//                 zoom: 11,
//               });
    
    // const plotParks = (parks) => {
    //             // array of parks, use marker to plot on map and fit bounds to center
    //         }
    //         // PlacesService(mapTarget.current)
    // const service = new window.google.maps.places.PlacesService(basicMap);
            
    //         // radius in meters so I added mile to radius, seems correct, formula pulled from SO ha
    // const radiusInMeters = (Math.round(10000*(radiusMiles*5280 / 3.281))/10000);
            
    // // location: mapTarget.current.getCenter()
    // service.nearbySearch(
    //     {location: basicMap.getCenter(), radius: radiusInMeters, type: ['playground']},
    //     (results, status, pagination) => {
    //         if (status !== 'OK' || !results.length) {
    //                     alert('No parks found near you, try increasing your radius or try a new address');
    //     } else {
    //         plotParks(results);
    //                 }
    //     });
   

// }})}



// function initMap() {
//     // Code that works with Google Maps here
//     document.querySelector('#playground-search').addEventListener('click', () => {
//         const userZip = prompt ('enter a zipcode');

//     //     const plotParks = (parks) => {
//     //     // array of parks, use marker to plot on map and fit bounds to center
//       // }
//       const basicMap = new google.maps.Map(document.querySelector('#map'), {
//         center: userZip,
//         zoom: 11,
//       });

//         const geocoder = new google.maps.Geocoder();
//         geocoder.geocode({ address: userZip }, (results, status) => {
//       if (status === 'OK') {
//         // Get the coordinates of the user's location
//         const userLocation = results[0].geometry.location;

//         // Create a marker
//         new google.maps.Marker({
//           position: userLocation,
//           map,
//         });

//         // Zoom in on the geolocated location
//         map.setCenter(userLocation);
//         map.setZoom(18);
//       } else {
//         alert(`Geocode was unsuccessful for the following reason: ${status}`);
//       }
//     });
//   });
//     const service = new window.google.maps.places.PlacesService(userLocation)
//     // const service = new window.google.maps.places.PlacesService(mapTarget.current);
    
//     // radius in meters so I added mile to radius, seems correct, formula pulled from SO ha
//     const radiusInMeters = (Math.round(10000*(radiusMiles*5280 / 3.281))/10000);
//     // const plotParks = (parks) => {
//     //     // array of parks, use marker to plot on map and fit bounds to center
//     // }
//     service.nearbySearch(
//         {location: userLocation.getCenter(), radius: radiusInMeters, type: ['playground']},
//         (results, status, pagination) => {
//             if (status !== 'OK' || !results.length) {
//                 alert('No parks found near you, try increasing your radius or try a new address');
//         } else {
//             plotParks(results);
//                     }
//         });
//   }