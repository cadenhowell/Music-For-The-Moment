import numpy as np

import listener.common as c
from listener.IBMWatson import SentimentAnalysis


# function takes in an utterance, and prints the response from the Watson API
def process_utterance(transcript):
    tones = SentimentAnalysis(transcript)
    if not tones:
        print("No tones found")
        return None
    sentiment_vec = np.zeros(7)
    for tone in tones:
        sentiment_vec[c.sentiment_dict[tone['tone_id']]] = tone['score']
    print(c.tones_to_string(tones))
    return sentiment_vec
