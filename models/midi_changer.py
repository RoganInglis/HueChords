"""
Need to -
- Load midi file
- Get chord on/off / time from midi
- Set up light control based on chord on/off / time
- Set up light envelopes based on chord on/off
- Play audio file and light track at the same time
"""

import ctypes
import models.utils as utils
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from phue import Bridge
import sounddevice as sd
import madmom.audio.signal as ms
import numpy as np
import sched
import time


class MidiHueController:
    def __init__(self):
        # Set some settings
        self.light_update_fs = 4*175/60
        self.envelope_ar = np.array([0.0001, 1/10])
        self.envelope_ar_rate = 1/self.envelope_ar
        self.brightness_envelope = True
        self.colour_envelope = True
        self.colour_envelope_depth = 5000

        self.audio_file_name = None
        self.audio_file = None
        self.audio_length = None
        self.hue_instructions = None

        self.chord_colour = {'C:maj': 0, 'C:min': 2849, 'C#:maj': 5698, 'C#:min': 8548, 'D:maj': 11397,
                             'D:min': 14246, 'D#:maj': 17096, 'D#:min': 19945, 'E:maj': 22794, 'E:min': 25644,
                             'F:maj': 28493, 'F:min': 31342, 'F#:maj': 34192, 'F#:min': 37041, 'G:maj': 39890,
                             'G:min': 42740, 'G#:maj': 45589, 'G#:min': 48438, 'A:maj': 51288, 'A:min': 54137,
                             'A#:maj': 56986, 'A#:min': 59836, 'B:maj': 62685, 'B:min': 65535}

        # Initialise lights
        self.b = Bridge('192.168.1.139')
        self.group = 2  # TODO - might want to change so that lights are controlled individually to allow different midi tracks to control different lights

    def load_track(self):
        # Get audio file
        Tk().withdraw()
        self.audio_file_name = askopenfilename(initialdir="C:\\Users\\Rogan Inglis\\OneDrive\\Documents\\Git Repositories\\HueChords\\data\\qualityaudio",
                                               title="Select audio file")

        self.audio_file, self.audio_fs = ms.load_audio_file(self.audio_file_name)

        self.audio_length = len(self.audio_file)/self.audio_fs

        # Get midi file
        Tk().withdraw()
        midi_file = askopenfilename(initialdir="C:\\Users\\Rogan Inglis\\OneDrive\\Documents\\Git Repositories\\HueChords\\data\\qualitymidi",
                                    title="Select midi file")

        # Process midi file
        self.hue_instructions = self.midi2hue_instructions(midi_file)

    def play(self):
        if (self.audio_file is None) and (self.hue_instructions is None):
            ctypes.windll.user32.MessageBoxW(0, u"No track loaded", u"No track loaded", 0)

        # Initialise lights
        self.b.set_group(self.group, 'on', True)
        self.b.set_group(self.group, 'sat', 254)

        self.b.set_group(self.group, self.hue_instructions[0]['command'])

        # Create scheduler
        scheduler = sched.scheduler()

        # Start audio file
        sd.play(self.audio_file, self.audio_fs, device=4)  # TODO - do this in a way that allows keeping track of time?

        # Set start time
        start_time = time.monotonic()

        # Control lights
        priority = len(self.hue_instructions) + 1
        for instruction in self.hue_instructions[1:]:
            # Double check so we don't schedule something for the past
            relative_instruction_time = instruction['time'] + start_time
            if time.monotonic() < relative_instruction_time:
                scheduler.enterabs(relative_instruction_time,
                                   priority,
                                   self.b.set_group,
                                   argument=(self.group, instruction['command']))

            priority -= 1

        # Add end of track instruction
        scheduler.enterabs(start_time + self.audio_length,
                           1,
                           self.b.set_group,
                           argument=(self.group, self.hue_instructions[-1]['command']))

        scheduler.run()
        # TODO - take into account delay of adding instructions to scheduler? seems minimal

    def play_no_scheduler(self):
        if (self.audio_file is None) and (self.hue_instructions is None):
            ctypes.windll.user32.MessageBoxW(0, u"No track loaded", u"No track loaded", 0)

        # Initialise lights
        self.b.set_group(self.group, 'on', True)
        self.b.set_group(self.group, 'sat', 254)

        command = self.hue_instructions[0]['command']
        self.b.set_group(self.group, command)

        # Start audio file
        sd.play(self.audio_file, self.audio_fs, device=4)  # TODO - do this in a way that allows keeping track of time?

        # Set start time
        start_time = time.monotonic()

        # Control lights
        prev_command = command
        while time.monotonic() <= start_time + self.audio_length:
            # Get most recent command
            for i, instruction in enumerate(self.hue_instructions):
                if (instruction['time'] + start_time) > time.monotonic():
                    command = self.hue_instructions[i - 1]['command']
                    break

            # Send command
            if prev_command != command:
                self.b.set_group(self.group, command)

            prev_command = command
            # Wait for some time
            time.sleep(0.01)

    def midi2hue_instructions(self, midi_file):
        chords = utils.midi2chords(midi_file, self.light_update_fs)

        # Iterate through chords and get non repeat instructions and add envelopes
        hue_instructions = []
        prev_chord = ""
        for chord in chords:
            # Ignoring envelopes for now
            if chord['chord'] is not prev_chord:
                if chord['chord'] is not "":
                    hue_instructions.append({'command': {'transitiontime': 0,
                                                         'bri': 254,
                                                         'hue': self.chord_colour[chord['chord']]},
                                             'time': chord['time']})
                else:
                    hue_instructions.append(
                        {'command': {'transitiontime': 0, 'bri': 0},
                         'time': chord['time']})
            prev_chord = chord['chord']

        return hue_instructions


if __name__ == '__main__':
    # Create midi hue controller class
    midiHueController = MidiHueController()

    # Load track
    midiHueController.load_track()

    # Play
    midiHueController.play()
