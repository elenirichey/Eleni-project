// const userZip = document.querySelector('#zipcode').value

const userZip = document.querySelector('#zipcode').innerText;
console.log(userZip)

const PLACEIDS = new Set();
const ALLPARKS = [];//or make it a set?
const keywords = ['playground', 'park'];

// okay so i want to map all the playgrounds from the list of playgrounds that my fetch
// request is getting, plus the manually added ones - can i add the manually added ones 
// somewhere besides the db so they can be recaptured if db is deleted? or can i 
// figure out how to search for multiple keywords
// TRY WITH TEXT SEARCH GOOGLE MAPS INSTEAD OF NEARBY PLACES??

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
        // lat: userLat, lng: userLng
        zoom: 13,
      });
      
      const locale = {'loc': userLocation, 'zipcode': userZip};
      const parkInfo = new google.maps.InfoWindow();
      // const requestOptions = {
      //   method:'POST',
      //   headers: {
      //     'Content-Type': 'application/json'
      //   },
      //   body: JSON.stringify(locale)
      // }

      for (const keyword of keywords) {
        fetch(`/local/${keyword}`, {
          method: 'POST',
          body: JSON.stringify(locale),
          headers: {
            'Content-Type': 'application/json'
          }    
        })   
          .then((response)=> response.json())
          .then((responseJson) => {
        console.log('line 16')
        for (const park of responseJson) {
          console.log(park, 'line 15')
          if (!PLACEIDS.has(park.place_id)) {
            ALLPARKS.push(park);
            PLACEIDS.add(park.place_id);
            console.log(ALLPARKS, 'line 62')}
      }  
        for (park of ALLPARKS) {
          console.log(park, 'line 78')
          const parkInfoContent = `
          <div class="window-content">
            <div class="park-thumbnail"></div>
      
            <ul class="park-info">
              <li><b>Park Geometry:</b>${park.geometry}</li>
              <li><b>Park Latitude:</b>${park.geometry.location['lat']}</li>
              <li><b>Park Latitude:</b>${park.geometry.location['lng']}</li>
              <li><b>Park Icon:</b>${park.icon}</li>
              <li><b>Park Name:</b>${park.name}</li>
              <li><b>Park Hours:</b>${park.opening_hours}</li>
              <li><b>Park Photos:</b>${park.photos}</li>
              <li><b>Park Address:</b>${park.vicinity}</li>
            </ul>
          </div>
        `;
        const parkMarker = new google.maps.Marker({
          position: {
            lat : park.geometry.location['lat'],
            lng: park.geometry.location['lng'],
          },
          title: `Park Name: ${park.name}`,
          map, // same as saying map: map
        }); 
        console.log(parkMarker, "line 103")
        parkMarker.addListener('click', () => {
          parkInfo.close();
          parkInfo.setContent(parkInfoContent);
          parkInfo.open(map, parkMarker);


        });
    } 


  

    console.log("line 76")
   } )}
  }})}