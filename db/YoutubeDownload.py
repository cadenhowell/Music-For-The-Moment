from youtube_dl import YoutubeDL

audio_downloader = YoutubeDL({'format': 'bestaudio'})

def youtube_downloader():
    URL = input('Plese Input a Youtube URL: ')

    try:
        # THIS IS PARAMS OBJECT FOR THE YOUTUBE DOWNLOADER
        # TO SEE MORE DOCUMENTATION TYPE youtube-dl -help in command line

        options = {
            'verbose': True,
            'audioformat': 'mp3',
            'outtmpl': './downloadedsongs/%(title)s.%(ext)s',
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            "restrictfilenames": True,
            "yesplaylist": True,
            "ignore-errors": True,
            # "batchfile": "/full/path/to/playlist"
        }

        print('Youtube Downloader'.center(40, '_'))

        audio_downloader.extract_info(URL)
        with YoutubeDL(options) as ydl:
            ydl.download([URL])

    except Exception:

        print("Couldn\'t download the audio")