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
