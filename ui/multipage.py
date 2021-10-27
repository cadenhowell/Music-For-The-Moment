import threading
from tkinter import *

from db import database
from db.corpus_generator import generate_corpus
from listener import main


class songbox():
    def __init__(self):
        self.songlist = {}

    def insert(self, i, songname, artist, filepath):
        if songname not in self.songlist:
            self.songlist[songname] = filepath
            songlistbox.insert(i, songname + ' by ' + artist)

    def delete(self, index, songname):
        songlistbox.delete(index)
        filepath = self.songlist[songname]
        del self.songlist[songname]
        database.delete(filepath, songname)


songbox1 = songbox()

# raises frame; puts first frame entry into second frame label
def raise_frame_for():
    result = entry1.get()
    if len(result) > 0:
        entry1.delete(0, END)
    else:
        label_too_large.config(text="Nothing was entered.")
    # get youtube url
    generate_corpus(result)
    songs = database.fetch_db()
    for index, songname in enumerate(songs.keys()):
        songbox1.insert(index, songname, songs[songname]['artist'], songs[songname]['file_name'])
    return


# changes the frame
def raise_frame_bac(frame):
    entry1.delete(0, END)
    frame.tkraise()


def deletesong():
    index = songlistbox.curselection()
    text = songlistbox.get(songlistbox.curselection())
    text = text.split(' by ')[0]
    print(text)
    # delete item from song corpus
    songbox1.delete(index, text)


def raise_frame(frame):
    frame.tkraise()


def listlabel_config():
    listlabel.config(text="Listening...")
    thread = threading.Thread(target=main.listener)
    thread.start()


root = Tk()
root.title('Music For the Moment')
root.geometry("500x500")

first_frame = Frame(root)
first_frame.place(x=0, y=0, width=500, height=500)

second_frame = Frame(root)
second_frame.place(x=0, y=0, width=500, height=500)

label_question = Label(first_frame, text="Please enter a Youtube playlist URL")
label_question.place(relx=0.5, rely=0.12, anchor=CENTER)

label_corp = Label(first_frame, text="Corpus of Songs:")
label_corp.place(relx=0.23, rely=0.4, anchor=CENTER)

label_too_large = Label(first_frame, text="")
label_too_large.place(relx=0.5, rely=0.32, anchor=CENTER)

entry1 = Entry(first_frame, width=20)
entry1.place(relx=0.5, rely=0.2, anchor=CENTER)

button_1 = Button(first_frame, text="Load Playlist", command=lambda: raise_frame_for())
button_1.place(relx=0.5, rely=0.27, anchor=CENTER)
button_2 = Button(second_frame, text="Manage Playlists", command=lambda: raise_frame_bac(first_frame)).place(x=10, y=10)

listimage = PhotoImage(file='./ui/listener.png').subsample(5)
button_6 = Button(second_frame, image=listimage, command=lambda: listlabel_config()).place(relx=0.3, rely=0.35)

listlabel = Label(second_frame, text="")
listlabel.place(relx=0.5, rely=0.7, anchor=CENTER)

button_3 = Button(first_frame, text="Listen", command=lambda: raise_frame(second_frame)).place(relx=0.8, y=10)

button_4 = Button(first_frame, text="Delete", command=lambda: deletesong()).place(relx=0.72, rely=0.37)

songlistbox = Listbox(first_frame, width=40, height=15, font=('calibri', 14))
songlistbox.place(relx=0.5, rely=0.7, anchor=CENTER)

root.mainloop()
