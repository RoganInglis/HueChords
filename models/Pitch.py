"""
Pitch functions
- Chroma
Last updated: 15 December 2012
from pymir - https://github.com/jsawruk/pymir
"""
from __future__ import division

import math

import numpy

# Dictionary of major and minor chords
chords = [{'name': "C:maj", 'vector': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], 'key': 0, 'mode': 1},
          {'name': "C:min", 'vector': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], 'key': 0, 'mode': 0},
          {'name': "C#:maj", 'vector': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], 'key': 1, 'mode': 1},
          {'name': "C#:min", 'vector': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 'key': 1, 'mode': 0},
          {'name': "D:maj", 'vector': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0], 'key': 2, 'mode': 1},
          {'name': "D:min", 'vector': [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0], 'key': 2, 'mode': 0},
          {'name': "D#:maj", 'vector': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], 'key': 3, 'mode': 1},
          {'name': "D#:min", 'vector': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0], 'key': 3, 'mode': 0},
          {'name': "E:maj", 'vector': [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], 'key': 4, 'mode': 1},
          {'name': "E:min", 'vector': [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], 'key': 4, 'mode': 0},
          {'name': "F:maj", 'vector': [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], 'key': 5, 'mode': 1},
          {'name': "F:min", 'vector': [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], 'key': 5, 'mode': 0},
          {'name': "F#:maj", 'vector': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0], 'key': 6, 'mode': 1},
          {'name': "F#:min", 'vector': [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0], 'key': 6, 'mode': 0},
          {'name': "G:maj", 'vector': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1], 'key': 7, 'mode': 1},
          {'name': "G:min", 'vector': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0], 'key': 7, 'mode': 0},
          {'name': "G#:maj", 'vector': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0], 'key': 8, 'mode': 1},
          {'name': "G#:min", 'vector': [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1], 'key': 8, 'mode': 0},
          {'name': "A:maj", 'vector': [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], 'key': 9, 'mode': 1},
          {'name': "A:min", 'vector': [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], 'key': 9, 'mode': 0},
          {'name': "A#:maj", 'vector': [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0], 'key': 10, 'mode': 1},
          {'name': "A#:min", 'vector': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], 'key': 10, 'mode': 0},
          {'name': "B:maj", 'vector': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1], 'key': 11, 'mode': 1},
          {'name': "B:min", 'vector': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1], 'key': 11, 'mode': 0}]


def cosineSimilarity(a, b):
    """
  Compute the similarity between two vectors using the cosine similarity metric
  """
    dotProduct = 0
    aMagnitude = 0
    bMagnitude = 0
    for i in range(len(a)):
        dotProduct += (a[i] * b[i])
        aMagnitude += math.pow(a[i], 2)
        bMagnitude += math.pow(b[i], 2)

    aMagnitude = math.sqrt(aMagnitude) + 0.0001
    bMagnitude = math.sqrt(bMagnitude) + 0.0001

    return dotProduct / (aMagnitude * bMagnitude)


def get_chord(chroma):
    """
  Given a chroma vector, return the best chord match using naive dictionary-based method
  """
    maxScore = 0
    chordName = ""
    for chord in chords:
        score = cosineSimilarity(chroma, chord['vector'])
        if score > maxScore:
            maxScore = score
            chordName = chord['name']

    return chordName, maxScore
