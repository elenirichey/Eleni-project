

const userZip = document.querySelector('#zipcode').innerText;


const PLACEIDS = new Set();
const ALLPARKS = [];
const keywords = ['playground', 'park'];


function initMap() {
  const geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: userZip }, (results, status) => {
    if (status === 'OK') {
     
      const userLocation = results[0].geometry.location;
      const userLat = results[0].geometry.location.lat();
      const userLng = results[0].geometry.location.lng();
      
      
      
      const map = new google.maps.Map(document.querySelector('#map'), {
        center: {lat: userLat, lng: userLng},
        
        zoom: 13
        
      });
      

      const locale = {'loc': userLocation, 'zipcode': userZip};
      
      const parkInfo = new google.maps.InfoWindow();
      

      
        fetch('/local/parks', {
          method: 'POST',
          body: JSON.stringify(locale),
          headers: {
            'Content-Type': 'application/json'
          }    
        })   
          .then((response)=> response.json())
          .then((responseJson) => {
        
        for (const park of responseJson) {
          
          if (!PLACEIDS.has(park.place_id)) {
            ALLPARKS.push(park);
            PLACEIDS.add(park.place_id);
            
          }
      }  
        for (park of ALLPARKS) {
          
          const parkInfoContent = `
          <div class="window-content">
            <div class="park-thumbnail"></div>
      
            <ul class="park-info">
              
              
               <b>${park.name}</b>
              <br>
              Address: <b>${park.formatted_address}</b>
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
        
        parkMarker.addListener('click', () => {
          parkInfo.close();
          parkInfo.setContent(parkInfoContent);
          parkInfo.open(map, parkMarker);


        })

        
        ;
    } 


  

    console.log("line 76")
   } )
  }})}