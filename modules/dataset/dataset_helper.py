import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Importing modules for paths and environment file
import os, sys, time

# Adding the project's root directory to the path
project_root = os.getcwd()
sys.path.append(f'{project_root}/data')
sys.path.append(f'{project_root}/src')

# Importing local modules
from json_helper.json_helper import dump_file, convert_numpy_types

# Initialising the paths for data files
spotify_data_path = f'{project_root}/src/data/Spotify_/'
log_data_path = f'{project_root}/src/data/logs/'
tracks_dataset_data_path = f'{project_root}/src/data/tracks_dataset/'


# Loading the dataset into code
df = pd.read_csv(f'{tracks_dataset_data_path}/dataset.csv', encoding= 'unicode_escape')

# Dropping unrealate columns
df.drop(['Unnamed: 0','track_id','artists','album_name','track_name','duration_ms','explicit','key','mode','valence','tempo','time_signature'], axis=1, inplace=True)

# Deleting null values
df.dropna(inplace=True)

# Group the DataFrame by the 'group' column
grouped = df.groupby('track_genre')

# Initialize an empty dictionary to store the results
genre_stats = {}

# Columns for which you want to calculate max, min, and mean
features_to_aggregate = ['popularity','danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness']

for genre, group in grouped:
    genre_dict = {}
    for feature in features_to_aggregate:
        genre_dict[feature] = {
            'max': group[feature].max(),
            'min': group[feature].min(),
            'mean': group[feature].mean()
        }
    genre_stats[genre] = genre_dict
    
from pprint import pprint
pprint(genre_stats,indent=4)

# Converting the values in the genre_stats dictionary to JSON supported encoding
convert_numpy_types(genre_stats)

# Saving the results to a JSON file
dump_file(f'{tracks_dataset_data_path}genre_stats.json', genre_stats)



