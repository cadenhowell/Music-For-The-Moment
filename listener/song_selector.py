import json
import os

import numpy as np
import requests

import listener.common as c
from db import database as db


def get_song(sentiment_vec, phrase, metric, sentiment_fract, n=None):
    """
    Returns the best song in the corpus given an utterance and its sentiment
    :param sentiment_vec: seven dim vec of 0-1 sentiment values
    :param phrase: the utterance
    :param metric: the distance metric to be used
    :param sentiment_fract: fractional weight of sentiment similarity (compared to 1-x weight of semantic similarity)
    :param n: number of songs to run semantic similarity on
    :return: json for the best song
    """
    data = db.fetch_db()
    songs, dist_scores = _get_n_closest(sentiment_vec, data, metric, n)
    similarity_scores = _get_similarity_scores(phrase, songs)
    scores = dist_scores * sentiment_fract + similarity_scores * (1 - sentiment_fract)
    idx = np.flip(np.argsort(scores))
    songs, dist_scores, similarity_scores, scores = songs[idx], dist_scores[idx], similarity_scores[idx], scores[idx]
    for i, song in enumerate(songs):
        print()
        print(f"Song {i + 1}/{len(songs)}")
        print(f"Title: {song['title']}")
        print(f"Artist: {song['artist']}")
        print(c.tones_to_string(song['watson']))
        print(f"Semantic Score: {dist_scores[i]:.3f} (Closer to 0 is better), Text Similarity Score: {similarity_scores[i]:.3f}")
        print(f"Total Score: {scores[i]:.3f}")
    print()
    return songs[np.argmax(scores)]


def _get_n_closest(sentiment_vec, data, method, n):
    n = len(data) if n is None else n
    songs = []
    dists = []
    for song in data:
        watson = data[song]['watson']
        dist, vect = 0, np.zeros(7)
        for sentiment in watson:
            id = sentiment['tone_id']
            vect[c.sentiment_dict[id]] = sentiment['score']
        if method == 'l1':
            dist = np.linalg.norm(vect - sentiment_vec, ord=1)
        elif method == 'l2':
            dist = np.linalg.norm(vect - sentiment_vec, ord=2)
        songs.append(data[song])
        dists.append(dist)
    songs = np.array(songs)
    dists = np.array(dists, dtype='float')
    dists = -dists
    n = len(songs) if n > len(songs) else n
    idx = np.argpartition(dists, -n)[-n:]
    return songs[idx], dists[idx]


def _get_similarity_scores(phrase, songs):
    scores = []
    for song in songs:
        lyrics = song['lyrics']
        scores.append(_similarity(phrase, lyrics))
    return np.array(scores, dtype='float')


def _similarity(text1, text2):
    url = "https://twinword-text-similarity-v1.p.rapidapi.com/similarity/"
    querystring = {
        "text1": text1,
        "text2": text2
    }
    headers = {
        'x-rapidapi-key': os.environ['RAPIDAI_KEY'],
        'x-rapidapi-host': "twinword-text-similarity-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    if response.status_code != 200:
        print("Error fetching text similarity from Twinword")
    return json_data['similarity']
