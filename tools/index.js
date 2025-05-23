/**
 * @license
 * Copyright 2024 Google LLC. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
/**
 * Demonstrates making a single request for Place predictions, then requests Place Details for the first result.
 */
async function init() {
  // @ts-ignore
  const { Place, AutocompleteSessionToken, AutocompleteSuggestion } =
    await google.maps.importLibrary("places");
  // Add an initial request body.
  let request = {
    input: "Cal",

    includedPrimaryTypes: ["restaurant"],
    language: "es",
    region: "mx",
  };
  // Create a session token.
  const token = new AutocompleteSessionToken();

  // Add the token to the request.
  // @ts-ignore
  request.sessionToken = token;

  // Fetch autocomplete suggestions.
  const { suggestions } =
    await AutocompleteSuggestion.fetchAutocompleteSuggestions(request);
  const title = document.getElementById("title");

  title.appendChild(
    document.createTextNode('Query predictions for "' + request.input + '":')
  );

  for (let suggestion of suggestions) {
    const placePrediction = suggestion.placePrediction;
    // Create a new list element.
    const listItem = document.createElement("li");
    const resultsElement = document.getElementById("results");

    listItem.appendChild(
      document.createTextNode(placePrediction.text.toString())
    );
    resultsElement.appendChild(listItem);
  }

  let place = suggestions[0].placePrediction.toPlace(); // Get first predicted place.

  await place.fetchFields({
    fields: ["displayName", "formattedAddress"],
  });

  const placeInfo = document.getElementById("prediction");

  placeInfo.textContent =
    "First predicted place: " +
    place.displayName +
    ": " +
    place.formattedAddress;
}

init();
