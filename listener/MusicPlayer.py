from pygame import mixer


class MusicPlayer:
    def __init__(self):
        self.music_file = ""
        self.playing_state = False

    def get_state(self):
        return self.playing_state

    def load(self, song_name):
        print('loading song')
        self.music_file = song_name

    def play(self):
        print('Playing song')
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()

    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
        else:
            mixer.music.unpause()
            self.playing_state = False

    def stop(self):
        mixer.music.stop()
