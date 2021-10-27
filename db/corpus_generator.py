import json
import os

import firebase_admin
import lyricsgenius
from dotenv import load_dotenv
from youtube_title_parse import get_artist_title

from db import database as db, YoutubeDownload
from listener.IBMWatson import SentimentAnalysis

load_dotenv()

token = os.environ['GENIUS_TOKEN']
genius = lyricsgenius.Genius(token)


def generate_file_name(filename):
    """
    fn to take a youtube-dl mp3 file, and convert to title_author
    :param filename: filename from youtube-dl mp3
    :return: artist, title
    """
    filename = filename.replace('_', ' ')
    filename = filename.replace('.mp3', '')
    filename = filename.replace('.', '')
    filename = filename.replace("'", '')
    artist, title = get_artist_title(filename)
    return artist, title



def generate_corpus(url):
    """
    Given a youtube playlist and directory of filenames, constructs corpus of songs,lyrics, and sentiment
    :param directory: path to directory of filenames generated by youtube-dl
    :return: None

    https://www.youtube.com/playlist?list=PLJD57x-QI7Q3Oy09MsXwM055nKu7b2B8A
    """

    YoutubeDownload.youtube_downloader(url)

    _, _, filenames = next(os.walk('../downloadedsongs'))

    try:
        songs = []
        for file in filenames:
            print(file)
            artist, title = generate_file_name(file)
            song = GetSongLyricsAndSentiment(title, artist)
            lyrics, watson = collectSongData(song)
            songs.append([title, artist, lyrics, watson, file])

        # write to corpus
        db.write(songs)

    except firebase_admin.exceptions.InvalidArgumentError:
        print("Firebase JSON Key Error")


def GetSongLyricsAndSentiment(song_name, artist_name):
    try:
        # Search song name and artist for lyrics on genius
        song = genius.search_song(song_name, artist_name)
        filename = artist_name.replace(' ', '_') + '_' + song_name.replace(' ', '_')
        song.save_lyrics(filename=filename)
        os.replace('./'+filename+'.json', './LyricGeniusData/' + filename + '.json')
        with open('./LyricGeniusData/'+filename + '.json') as f:
            return json.load(f)

    except AttributeError:
        print('Song could not be processed')

    finally:
        _, _, filenames = next(os.walk('../LyricGeniusData/'))
        extensions = [file.split('.')[-1] for file in filenames]
        for i, extension in enumerate(extensions):
            if extension == 'json':
                os.remove('./LyricGeniusData/' + filenames[i])


def collectSongData(adic):
    lyrics = adic['lyrics']  # song lyrics

    # FUNCTION TO GET ONLY LYRICS
    helper_string = ''
    add_to_substring = False
    for index, char in enumerate(lyrics):
        if char == '[':
            add_to_substring = True
        if add_to_substring:
            helper_string += char
        if char == ']':
            lyrics = lyrics.replace(helper_string, '')
            helper_string = ''
            add_to_substring = False

    watson = SentimentAnalysis(lyrics)
    return lyrics, watson