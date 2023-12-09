from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_song_data():
    data = request.get_json()
    genre = data['genre']
    acousticness = data['acousticness']
    danceability = data['danceability']
    instrumentalness = data['instrumentalness']
    energy = data['energy']
    numberOfsongs = data['numberOfsongs']
    filtered_df = df[(df['genre'] == genre) &
                      (df['acousticness'] >= acousticness[0]) &
                      (df['acousticness'] <= acousticness[1]) &
                      (df['danceability'] >= danceability[0]) &
                      (df['danceability'] <= danceability[1]) &
                      (df['instrumentalness'] >= instrumentalness[0]) &
                      (df['instrumentalness'] <= instrumentalness[1]) &
                      (df['energy'] >= energy[0]) &
                      (df['energy'] <= energy[1])]

    filtered_df = filtered_df.head(numberOfsongs)

    return jsonify(filtered_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
