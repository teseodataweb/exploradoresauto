function iniciarMap() {
  var coord = { lat: 20.1056307, lng: -98.7879191 };
  var map = new google.maps.Map(document.getElementById("map"), {
    center: coord,
    zoom: 16,
  });
  var marker = new google.maps.Marker({
    position: coord,
    map: map,
    title: "4to Creativo",
  });
}

// Add an initial request body.
let request = {
  input: "Tadi",
  locationRestriction: {
    west: -122.44,
    north: 37.8,
    east: -122.39,
    south: 37.78,
  },
  origin: { lat: 37.7893, lng: -122.4039 },
  includedPrimaryTypes: ["restaurant"],
  language: "en-US",
  region: "us",
};
// Create a session token.
const token = new AutocompleteSessionToken();

// Add the token to the request.
// @ts-ignore
request.sessionToken = token;
