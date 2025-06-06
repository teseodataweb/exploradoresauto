const placeInput = document.getElementById("place-input");
let map;
let autocomplete;

window.initMap = function () {
  const coords = { lat: 19.406940428320986, lng: -99.14819687896599 };
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 6,
    center: coords,
  });

  const marker = new google.maps.Marker({
    position: coords,
    map,
  });

  searchGoogleMap();
};

const searchGoogleMap = () => {
  autocomplete = new google.maps.places.Autocomplete(placeInput);
  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    map.setCenter(place.geometry.location);
    map.setZoom(13);
  });
};
