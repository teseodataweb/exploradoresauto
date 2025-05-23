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

function initAutocomplete() {
  const input = document.getElementById("pac-input");
  const autocomplete = new google.maps.places.Autocomplete(input, {
    fields: ["place_id", "geometry", "name"],
  });
  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    // Aquí puedes acceder a la información del lugar (place)
    console.log(place);
    // Puedes actualizar el mapa para mostrar el lugar
  });
}

function searchNearby(map, center) {
  const placesService = new google.maps.places.PlacesService(map);
  const request = {
    location: center,
    radius: 500, // Radio de búsqueda
    types: ["restaurant"], // Ejemplo: restaurantes
  };
  placesService.nearbySearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      // Procesar los resultados (results)
      results.forEach((result) => {
        // Crear un marcador para cada lugar
        new google.maps.Marker({
          map: map,
          position: result.geometry.location,
          title: result.name,
        });
      });
    }
  });
}
