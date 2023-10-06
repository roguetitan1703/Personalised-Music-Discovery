document.addEventListener("DOMContentLoaded", function () {
    const generateButton = document.getElementById("generateButton");
    generateButton.addEventListener("click", generatePlaylist);
});
const quantityInput = document.getElementById('quantity');
quantityInput.addEventListener('keydown', (event) => {
  event.preventDefault();
});

function generatePlaylist() {
    const genre = document.getElementById("genre").value;
    const acousticness = document.getElementById("acousticness").value;
    const danceability = document.getElementById("danceability").value;
    const instrumentalness = document.getElementById("instrumentalness").value;
    const energy = document.getElementById("energy").value;
    const numberOfSongs = document.getElementById("numberOfSongs").value;

    //add the flask wala here

    const playlist = document.getElementById("playlist");
    playlist.innerHTML = `
        <h2>Generated Playlist</h2>
        <p>Genre: ${genre}</p>
        <p>Acousticness: ${acousticness}</p>
        <p>Danceability: ${danceability}</p>
        <p>Instrumentalness: ${instrumentalness}</p>
        <p>Energy: ${energy}</p>
        <p>Number of Songs: ${numberOfSongs}</p>
    `;
 
}