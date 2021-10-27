import threading

import speech_recognition as sr

import listener.song_selector as song_selector
import listener.tone_analyzer as tone_analyzer
from db import database
from listener.MusicPlayer import MusicPlayer

music_player = MusicPlayer()
r = sr.Recognizer()
current_song, next_song = None, None


def worker(transcript):
    sentiment_vec = tone_analyzer.process_utterance(transcript)
    if sentiment_vec is not None:
        best_song = song_selector.get_song(sentiment_vec, transcript, 'l2', .75, None)
        songs_dict = database.fetch_db()
        file_path = songs_dict[best_song['title']]['file_name']
        global next_song, current_song
        next_song = './downloadedsongs/' + file_path.lower()
        if next_song and next_song != current_song:
            music_player.load(next_song)
            current_song = next_song
            music_player.play()


# Reading Microphone as source
# listening the speech and store in audio_text variable
def listener():
    while True:
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.record(source, duration=8)
            print("Utterance recorded. Calling Watson.")
            try:
                # using google speech recognition
                transcript = r.recognize_google(audio_text)
                print("\nText: " + transcript)
                # opens up a thread to call the watson API as a separate process
                thread = threading.Thread(target=worker, args=(transcript,))
                thread.start()
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
