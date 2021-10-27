import lyricsgenius
import os
import json
from IBMWatson import SentimentAnalysis
from dotenv import load_dotenv
import database as db

load_dotenv()

token = os.environ['GENIUS_TOKEN']
genius = lyricsgenius.Genius(token)

# def format_filename(artist_name, song_name):



def GetSongLyricsAndSentiment(song_name, artist_name):
    try:
        # Search song name and artist for lyrics on genius
        song = genius.search_song(song_name, artist_name)

        filename = artist_name.replace(' ', '_') + '_' + song_name.replace(' ', '_')
        song.save_lyrics(filename=filename)
        os.replace('./'+filename+'.json', './LyricGeniusData/' + filename + '.json')
        with open('./LyricGeniusData/'+filename + '.json') as f:
            Song = json.load(f)

            # Create an empty dictionary to store your songs and related data

            def collectSongData(adic):
                dps = list()
                title = adic['title']  # song title
                artist = adic['primary_artist']['name']  # artist name(s)
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
                # print(watson)
                dps.append((title, artist, lyrics))  # append all to one tuple list

                with open("./songs.json", 'r+') as json_file:
                    data = json.load(json_file)
                    data[title] = {
                        'title': title,
                        'artist': artist,
                        'lyrics': lyrics,
                        'watson': watson
                    }
                    json_file.seek(0)
                    json.dump(data, json_file, indent=4)
                    json_file.truncate()  # remove remaining part

            collectSongData(Song)  # check function works
    except AttributeError:
        print('Song could not be processed')

    finally:
        _, _, filenames = next(os.walk('./LyricGeniusData/'))
        print(filenames)
        extensions = [file.split('.')[-1] for file in filenames]
        print(extensions)
        for i, extension in enumerate(extensions):
            if extension == 'json':
                print(filename)
                os.remove('./LyricGeniusData/' + filenames[i])


def get_corpus_lyrics_and_sentiment():
    corpus = db.fetch_db()
    # print(corpus)
    for song, song_data in corpus.items():
        song_name = song
        artist = song_data['artist']
        GetSongLyricsAndSentiment(song_name, artist)


# get_corpus_lyrics_and_sentiment()
