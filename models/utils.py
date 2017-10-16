import pretty_midi
import matplotlib.pyplot as plt
from models.Pitch import get_chord
import numpy as np


def midi2chords(midi_file, fs):
    """
    Loads a specified midi file and works out the chords and their timings
    :param midi_file: midi file path
           fs: sample rate to get chords at
    :return: chords - a list of tuples of form (chord, on/off, time)
    """
    # Load midi file
    mid = pretty_midi.PrettyMIDI(midi_file)

    ts = 1/fs

    # Get chroma vectors
    chroma_vectors = mid.get_chroma(fs)
    chroma_vectors = np.transpose(chroma_vectors/np.amax(chroma_vectors), [1, 0])

    chords = []
    sample = 0
    for chroma_vector in chroma_vectors:
        chords.append({'chord': get_chord(chroma_vector)[0], 'time': ts*sample})
        sample += 1

    return chords


if __name__ == "__main__":
    midi_file = "C:\\Users\\Rogan Inglis\\OneDrive\\Documents\\Git Repositories\\HueChords\\data\\qualitymidi\\out_the_blue.mid"
    chords = midi2chords(midi_file, 10)
