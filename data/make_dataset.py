from midi2audio import FluidSynth
import os

# midi_path = os.getcwd() + "\\midi\\"
midi_path = os.getcwd() + "\\"

for file in os.listdir(midi_path):
    if file.endswith('.mid'):
        print(midi_path + file)
        FluidSynth().play_midi(midi_path + file)
