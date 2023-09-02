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

# Get the recommendation tracks with the SpotifyAPIGetRecommendations method get_recommendations_spotify
def get_recommendation_tracks():
      
      # Creating a parameters dictionary to manage high number of params passing into the get_recommendation_spotify() function 
      recommendation_parameters = {
            'limit': limit.get(),
            'seed_genres': genre.get().lower(),
            # 'seed_artist': '',
            # 'seed_tracks': '',
            'target_acousticness' : acousticness.get(),
            'target_danceability' : danceability.get(),
            'target_instrumentalness' : instrumentalness.get(),
            'target_energy' : energy.get()
            }
      
      # Get the playlist from the get_recommendation_spotify method
      playlist = SpotifyAPIUtility.get_recommendations_spotify(parameters=recommendation_parameters)
      
      # Make the track_uris array which contains uri of all the tracks in the playlist
      # R// refer the function SpotifyAPIUtility.get_recommendation_spotify() for the format of the data stored in the array playlist 
      playlist_creation_parameters = {
            'playlist_name' : f'{genre.get()} Playlist',
            'playlist_description' : f'This is a playlist of {genre.get()} songs created by Personalised Music Discovery Project',
            'track_uris' : [track['track_uri'] for track in playlist]
      }
      
      # Create a playlist in the user's Spotify account
      created_playlist = SpotifyAPIUtility.create_and_add_to_playlist(parameters=playlist_creation_parameters)
      
      if created_playlist['is_playlist_created']:
            print(f'{genre.get()} Playlist Created Successfully')
            print(f'Playlist url: {created_playlist["playlist_url"]}')

      else:
            print('Playlist Creation Failed')
      # # Print the data sent to the function
      # print('Genre: ',genre.get())
      # print('Acousticness: ',acousticness.get())
      # print('Danceability: ',danceability.get())
      # print('Instrumentalness: ',instrumentalness.get())
      # print('Energy: ',energy.get())
      # print('Number of Songs: ',limit.get())
      # print('\n')
      
      # # Printing Playlist
      # ctr = 0
      # for track in playlist:
      #       ctr += 1
      #       artists_name = ', '.join([artist['artist_name'] for artist in track['artists']])
      #       print(f"{ctr}. {track['track_name']} by {artists_name}")
            


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
Label(root, text='Discover Music', width=32,
      anchor='center', justify='center',
      font=('Helvetica', 15),
      background='#248847', foreground='#ffffff').grid(row=0,columnspan=2)

# Creating a genre selector dropdown menu

# Creating a label for the dropdown menu
Label(root, text='Select a genre:',
      width=27, anchor='e', justify='right',
      font=('Helvetica', 10)).grid(row=1,column=0,pady=5)

# Combobox creation
genre = StringVar()
genrechosen = Combobox(root, width=15, textvariable=genre)

# Adding values to the dropdown
genrechosen['values'] = ('Rock',
                         'Pop',
                         'Edm')

genrechosen['state'] = 'readonly'
genrechosen.current(2)
genrechosen.grid(row=1, column=1)

# Creating a scale widget for various music features values

# Creating acousticness selector widget

# Creating the label for the acousticness selector
Label(root, text='Select Acousticness range:',
      width=27, anchor='e', justify='right',
      font=('Helvetica', 10)).grid(row=2,column=0)

# Creating the scale widget for the acousticness selector

acousticness = DoubleVar()
acn = Scale(root, variable=acousticness,
            from_=0, to=1, orient=HORIZONTAL)

acn.grid(row=2, column=1)

# Creating danceability selector widget

# Creating the label for the danceability selector

Label(root, text='Select Danceability range:',
      width=27, anchor='e', justify='right',
      font=('Helvetica', 10)).grid(row=3,column=0)

# Creating the scale widget for the danceability selector

danceability = DoubleVar()
dn = Scale(root, variable=danceability,
            from_=0, to=1, orient=HORIZONTAL)

dn.grid(row=3, column=1)


# Creating instrumentalness selector widget

# Creating the label for the instrumentalness selector

Label(root, text='Select Instrumentalness range:',
      width=27, anchor='e', justify='right',
      font=('Helvetica', 10)).grid(row=4,column=0)

# Creating the scale widget for the instrumentalness selector

instrumentalness = DoubleVar()
ins = Scale(root, variable=instrumentalness,
            from_=0, to=1, orient=HORIZONTAL)

ins.grid(row=4, column=1)

# Creating energy selector widget

# Creating the label for the energy selector

Label(root, text='Select Energy range:',
      width=27, anchor='e', justify='right',
      font=('Helvetica', 10)).grid(row=5,column=0)

# Creating the scale widget for the energy selector

energy = DoubleVar()
en = Scale(root, variable=energy,
            from_=0, to=1, orient=HORIZONTAL)

en.grid(row=5, column=1)

# Creating a number of songs spinbox

# Creating the label for the number of songs

Label(root, text='Select number of songs:',
      width=27, anchor='e', justify='right',
      font=('Helvetica', 10)).grid(row=6,column=0)

# Creating the number of songs spinbox 
limit = IntVar()
nos = Spinbox(root, from_=0, to=20, textvariable=limit)
nos['state'] = 'readonly'
nos.grid(row=6, column=1)

# Creating a search button

discover_music  = Button(root, text='Discover', command= get_recommendation_tracks, width=10)
discover_music.grid(row=7,columnspan=2)


    
root.mainloop()