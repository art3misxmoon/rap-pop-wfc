import mido

# step 1: translating the midi file

midi = mido.MidiFile('3005.mid') # defines the file as a MidiFile type

# prints each message from the midi file tracks. 
# note-on turns the note on, note-off turns the note off. 
# note, in this case, is which instrument is playing. 
# time is the time since the last msg (24 time = 1/16 note). 
# channel and velocity are not relevant for now. 
# docs: https://mido.readthedocs.io/en/latest/messages.html#control-changes
for i, track in enumerate(midi.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

# step 2: parse the MidiFile and translate to a structure we can use
# 1 array for each instrument, and each element of the array representing 24 units of time. 
# each element of the array is either:
# a string "off" meaning the instrument isn't playing
# a string "on-off" meaning the instrument stops on that beat
# a string "on" meaning the instrument is playing
# a string "off-on" meaning the instrument starts on that beat

numberOfInstruments = 12
playing = [False for i in range(numberOfInstruments)]
timelines = [[] for i in range(numberOfInstruments)]
instrument = 0
time = 0 # time attribute, in special units
lastFill = 0 # index of last fill of empty spots

for i, track in enumerate(midi.tracks):
    print('Track {}: {}'.format(i, track.name))
    for index, msg in enumerate(track):
        time += int(msg.time) # updates time attribute
        if msg.is_meta: # throw out if message is metainfo
            continue
        instrument = msg.note-36 # chooses corresponding instrument to message
        if msg.type == "note_off": 
            for i in range(lastFill, int(time/24)): # fills in all spots until instrument state change
                timelines[instrument].append("on")
            timelines[instrument].append("on-off") # turns instrument off
        elif msg.type == "note_on": 
            for i in range(lastFill, int(time/24)): # fills in all spots until instrument state change
                timelines[instrument].append("off")
            timelines[instrument].append("off-on") # turns instrument on
        playing[instrument] = not playing[instrument]

        if track[index + 1].time != 0: # if there aren't anymore instruments to change the status of at this time
            for i in range(lastFill, int(time/24)+1): # for all indices since last fill
                for j in range(len(playing)): # for all instruments
                    if playing[j] == True and len(timelines[j]) < (time/24): # if playing and not one of the updated instruments
                        timelines[j].append("on")
                    if playing[j] == False and len(timelines[j]) < (time/24): # if not playing and not one of the updated instruments
                        timelines[j].append("off")
            lastFill = int(time/24) + 1 # update fill time

# from bottom to top, yeah = bell = bigSynth = alarm = highSynth = backgroundVocals = ahAh = snare = bass = bongo = spaceySynth = synth
for i in timelines:
    str = "::::: "
    for e in i[:20]:
        str += ''.join(format(e,'>8'))
    print(str)

# step 3: make a list of 'blocks', representing every possible 1/4 note segment (96 units of time)
# each block contains a two-item array for each instrument, with each element a string (same definitions as above)
# each element of the array represents one of four subdivisions, or a 1/16 note
# in addition, it should contain two arrays, each one containing possibles adjacencies before/after the block.

class Block:
    def __init__(name, yeah, bell, bigSynth, alarm, highSynth, backgroundVocals, ahAh, snare, bass, bongo, spaceySynth, synth, adjacencies1):
        self.id = name
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
