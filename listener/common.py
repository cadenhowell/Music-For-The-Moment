sentiment_dict = {
    'tentative': 0,
    'fear': 1,
    'anger': 2,
    'joy': 3,
    'confident': 4,
    'sadness': 5,
    'analytical': 6,
}


def tones_to_string(tones):
    song_semantics = 'Semantics: '
    for tone in tones:
        song_semantics += f"{tone['tone_name']}: {tone['score']:.3f}, "
    return song_semantics.strip(', ')
