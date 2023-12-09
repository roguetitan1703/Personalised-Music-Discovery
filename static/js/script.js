document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("discover-button").addEventListener("click", function() {
        // Get data from the form
        var genre = document.getElementById("genre").value;
        // Convert string values to floats
        var acousticness = parseFloat(document.getElementById("acousticness").value);
        var speechiness = parseFloat(document.getElementById("speechiness").value);
        var danceability = parseFloat(document.getElementById("danceability").value);
        var instrumentalness = parseFloat(document.getElementById("instrumentalness").value);
        var energy = parseFloat(document.getElementById("energy").value);
        // Convert limit to integer if needed
        var limit = parseInt(document.getElementById("limit").value);

        // create data
        var data = {
            seed_genres: genre,
            target_acousticness: acousticness,
            target_speechiness: speechiness,
            target_danceability: danceability,
            target_instrumentalness: instrumentalness,
            target_energy: energy,
            limit: limit
        };

        // Make an HTTP POST request to the server
        fetch('/discover-music', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.text())  // Assuming the server returns HTML as plain text
        .then(htmlSnippet => {
            // Update the "results" div with the received HTML snippet
            document.getElementById("results").innerHTML = htmlSnippet;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
