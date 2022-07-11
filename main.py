import mido

# step 1: translating the midi file

midi = mido.MidiFile('3005.mid') # defines the file as a MidiFile type

# prints each message from the midi file tracks. 
# note-on turns the note on, note-off turns the note off. 
# note, in this case, is which instrument is playing. 
# time is the time since the last msg (16 time = 1/4 note). 
# channel and velocity are not relevant for now. 
# docs: https://mido.readthedocs.io/en/latest/messages.html#control-changes
for i, track in enumerate(midi.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

# step 2: parse the MidiFile and translate to a structure we can use
# 1 array for each instrument, and each element of the array representing 8 units of time. 
# each element of the array is either:
# a string "off" meaning the instrument isn't playing
# a string "on-off" meaning the instrument stops on that beat
# a string "on" meaning the instrument is playing
# a string "off-on" meaning the instrument starts on that beat

numberOfInstruments = 12
playing = [False for i in range(numberOfInstruments)]
timelines = [[] for i in range(numberOfInstruments)]
instrument = 0

for i, track in enumerate(midi.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        if msg.is_meta: # checks if message is metainfo
            continue
        if msg.time > 8: # checks if time elapsed is longer than an eighth note
            for i in range(int(msg.time/8)): # for each eighth note missed
                for j in range(len(playing)): # for each instrument
                    if playing[j] == True:
                        timelines[j].append("on")
                    if playing[j] == False:
                        timelines[j].append("off")
        instrument = msg.note-36 # chooses corresponding instrument to message
        if msg.type == "note_off": # turns instrument off
            timelines[instrument].append("on-off")
            playing[instrument] = not playing[instrument]
        elif msg.type == "note_on": # turns instrument on
            timelines[instrument].append("off-on")
            playing[instrument] = not playing[instrument]

# from bottom to top, yeah = bell = bigSynth = alarm = highSynth = backgroundVocals = ahAh = snare = bass = bongo = spaceySynth = synth
for i in timelines:
    str = "::::: "
    for e in i[:20]:
        str += e + " "
    print(str)

# step 3: make a list of 'blocks', representing every possible 1/4 note segment (16 units of time)
# each block contains a two-item array for each instrument, with each element a string (same definitions as above)
# each element of the array represents one of two subdivisions, or an 1/8 note
# in addition, it should contain two arrays, each one containing possibles adjacencies before/after the block.

class Block:
    def __init__(yeah, bell, bigSynth, alarm, highSynth, backgroundVocals, ahAh, snare, bass, bongo, spaceySynth, synth, adjacencies1):
        self.yeah = yeah
        self.bell = bell
        self.bigSynth = bigSynth
        self.alarm = alarm
        self.highSynth = highSynth
        self.backgroundVocals = backgroundVocals
        self.ahAh = ahAh
        self.snare = snare
        self.bass = bass
        self.bongo = bongo
        self.spaceySynth = spaceySynth
        self.synth = synth
        self.adjacencies1 = adjacencies1
