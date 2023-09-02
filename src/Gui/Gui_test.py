# Importing gui
from tkinter import *
from tkinter.ttk import *
from tkinter import IntVar

# Importing other modules
import os, sys
from urllib.parse import urlencode

# Adding the project's root directory to the path
project_root = os.getcwd()
sys.path.append(f'{project_root}/data')
sys.path.append(f'{project_root}/src')

# Import local modules
from Spotify_.SpotifyAPI import SpotifyAPIUtility
from helpers_.json_helper import dump_file, read_file

spotify_data_path = f'{project_root}/src/data/Spotify_/'

# To save the playlists details locally
def save_playlist(playlist, playlist_file=f'{spotify_data_path}/playlists.json'):
      # Fetching already saved playlist details if any
      playlists = read_file(playlist_file)
      
      # Checking if playlist details are already there
      if playlists:
            playlists.append(playlist)
      # If not then creating a new list and adding the playlist details
      else:
            playlists = [playlist]
            
      # Saving the details into the files
      dump_file(playlist_file, playlists)
      
            
# Get the recommendation tracks with the SpotifyAPIGetRecommendations method get_recommendations_spotify
def get_recommendation_tracks():
      
      # Creating a parameters dictionary to manage high number of params passing into the get_recommendation_spotify() function 
      recommendation_parameters = {
            'limit': tracks_limit_var.get(),
            'seed_genres': genre_choice_var.get().lower(),
            # 'seed_artist': '',
            # 'seed_tracks': '',
            'target_acousticness' : acousticness_selector_var.get(),
            'target_speechiness' : speechiness_selector_var.get(),
            'target_danceability' : danceability_selector_var.get(),
            'target_instrumentalness' : instrumentalness_selector_var.get(),
            'target_energy' : energy_selector_var.get()
            }
      
      # Get the playlist from the get_recommendation_spotify method
      tracks_array = SpotifyAPIUtility.get_recommendations_spotify(parameters=recommendation_parameters)
      
      # Make the track_uris array which contains uri of all the tracks in the playlist
      # R// refer the function SpotifyAPIUtility.get_recommendation_spotify() for the format of the data stored in the array playlist 
      playlist_creation_parameters = {
            'playlist_name' : f'{genre_choice_var.get()} Playlist',
            'playlist_description' : f'This is a playlist of {genre_choice_var.get()} songs created by Personalised Music Discovery Project',
            'track_uris' : [track['track_uri'] for track in tracks_array]
      }
      
      # Create a playlist in the user's Spotify account
      created_playlist = SpotifyAPIUtility.create_and_add_to_playlist(parameters=playlist_creation_parameters)
      
      if created_playlist['is_playlist_created']:
            print(f'{genre_choice_var.get()} Playlist Created Successfully')
            print(f'Playlist url: {created_playlist["playlist_url"]}')

      else:
            print('Playlist Creation Failed')
      
      # Save the playlist details locally
      save_playlist(created_playlist)      


# Creating a root windiow
root = Tk()

# Creating a window
root.title("Music Discovery Project")
root.geometry('350x250')
root.resizable(False,False)

# Initializing styles
s = Style()
s.configure('search.TButton', font=('Helvetica', 10), background='#248847', activebackground='#25653b')



# Main title text label
top_heading = Label(root, text='Discover Music', width=32,
                        anchor='center', justify='center',
                        font=('Helvetica', 15),
                        background='#248847', foreground='#ffffff').grid(row=0,columnspan=2)


      
# Creating a genre selector dropdown menu

# Creating a label for the dropdown menu
genre_choice_label = Label(root, text='Select a genre:',
                        width=27, anchor='e', justify='right',
                        font=('Helvetica', 10)).grid(row=1,column=0,pady=5)

# Combobox creation
genre_choice_var = StringVar()
genre_choice = Combobox(root, width=15, textvariable=genre_choice_var)

# Adding values to the dropdown
genre_choice['values'] = ('Deep-house',
                        'Edm',
                        'Electronic',
                        'Hip-hop',
                        'House',
                        'Metal-core',
                        'Pop',
                        'Rock',
                        'Synth-pop',)

genre_choice['state'] = 'readonly'
genre_choice.current(0)
genre_choice.grid(row=1, column=1)

# Creating a scale widget for various music features values

# Creating acousticness selector widget

# Creating the label for the acousticness selector
acousticness_selector_label = Label(root, text='Select Acousticness range:',
                                    width=27, anchor='e', justify='right',
                                    font=('Helvetica', 10)).grid(row=2,column=0)


# Creating the scale widget for the acousticness selector

acousticness_selector_var = DoubleVar()
acousticness_selector = Scale(root, variable=acousticness_selector_var,
                              from_=0, to=1, orient=HORIZONTAL)

acousticness_selector.grid(row=2, column=1)

# Creating speechiness selector widget

# Creating the label for the speechiness selector

speechiness_selector_label = Label(root, text='Select Speechiness range:',
      width=27, anchor='e', justify='right',
      font=('Helvetica', 10)).grid(row=3,column=0)

# Creating the scale widget for the speechiness selector

speechiness_selector_var = DoubleVar()
speechiness_selector = Scale(root, variable=speechiness_selector_var,
                              from_=0, to=1, orient=HORIZONTAL)

speechiness_selector.grid(row=3, column=1)

# Creating danceability selector widget

# Creating the label for the danceability selector

danceability_selector_label = Label(root, text='Select Danceability range:',
                                    width=27, anchor='e', justify='right',
                                    font=('Helvetica', 10)).grid(row=4,column=0)

# Creating the scale widget for the danceability selector

danceability_selector_var = DoubleVar()
danceability_selector = Scale(root, variable=danceability_selector_var,
                              from_=0, to=1, orient=HORIZONTAL)

danceability_selector.grid(row=4, column=1)

# Creating instrumentalness selector widget

# Creating the label for the instrumentalness selector

instrumentalness_selector_label = Label(root, text='Select Instrumentalness range:',
                                          width=27, anchor='e', justify='right',
                                          font=('Helvetica', 10)).grid(row=5,column=0)

# Creating the scale widget for the instrumentalness selector

instrumentalness_selector_var = DoubleVar()
instrumentalness_selector = Scale(root, variable=instrumentalness_selector_var,
                                    from_=0, to=1, orient=HORIZONTAL)

instrumentalness_selector.grid(row=5, column=1)

# Creating energy selector widget

# Creating the label for the energy selector

energy_selector_label = Label(root, text='Select Energy range:',
                              width=27, anchor='e', justify='right',
                              font=('Helvetica', 10)).grid(row=6,column=0)

# Creating the scale widget for the energy selector

energy_selector_var = DoubleVar()
energy_selector = Scale(root, variable=energy_selector_var,
                        from_=0, to=1, orient=HORIZONTAL)

energy_selector.grid(row=6, column=1)

# Creating a number of songs spinbox

# Creating the label for the number of songs

tracks_limit_label = Label(root, text='Select number of songs:',
                              width=27, anchor='e', justify='right',
                              font=('Helvetica', 10)).grid(row=7,column=0)

# Creating the number of songs spinbox 
tracks_limit_var = IntVar()
tracks_limit = Spinbox(root, from_=0, to=50, textvariable=tracks_limit_var, wrap=True)
tracks_limit['state'] = 'readonly'
tracks_limit.grid(row=7, column=1)

# Creating a search button

discover_music  = Button(root, text='Discover', command= get_recommendation_tracks, width=10)
discover_music.grid(row=8,columnspan=2)

root.mainloop()
