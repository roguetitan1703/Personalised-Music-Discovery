from tkinter import *
from tkinter.ttk import *
from tkinter import IntVar


# get the music
def get_music():
    print('Genre: ',genre.get())
    print('Acousticness: ',acousticness.get())
    print('Danceability: ',danceability.get())
    print('Instrumentalness: ',instrumentalness.get())
    print('Energy: ',energy.get())
    print('Number of Songs: ',number_of_songs.get())
    


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
number_of_songs = IntVar()
nos = Spinbox(root, from_=0, to=20, textvariable=number_of_songs)
nos['state'] = 'readonly'
nos.grid(row=6, column=1)

# Creating a search button

discover_music  = Button(root, text='Discover', command= get_music, width=10)
discover_music.grid(row=7,columnspan=2)


    
root.mainloop()