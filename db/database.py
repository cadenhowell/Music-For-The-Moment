import os

from firebase_admin import db

from db.firebase_config import ref


# gets songs in specific corpus
def fetch_db(corpus_name='corpus_1'):
    return db.reference('/' + corpus_name + '/').get()


def fetch_specific(path):  # for specific song
    return db.reference(path).get()


def delete(filepath, songname, corpus_name='corpus_1'):
    os.remove('./downloadedsongs/' + filepath)
    return ref.child(corpus_name + '/' + songname + '/').set({})


def write(songs, corpus_name='corpus_1'):
    for i, song in enumerate(songs):
        obj = {
            song[0]: {
                "artist": song[1],
                "title": song[0],
                "lyrics": song[2],
                "watson": song[3],
                "file_name": song[4]
            }
        }
        ref.child(corpus_name + '/').update(obj)
