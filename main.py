import mido

# step 1: translating the midi file

midi = mido.MidiFile('3005.mid') # defines the file as a MidiFile type

# prints each message from the midi file tracks. 
# note-on turns the note on, note-off turns the note off. 
# note, in this case, is which instrument is playing. 
# time is the time since the last msg (24 time = 1/16 note). 
# channel and velocity are not relevant for now. 
# docs:
# https://mido.readthedocs.io/en/latest/messages.html#control-changes
for i, track in enumerate(midi.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

# step 2: parse the MidiFile and translate to a structure we can use
# 1 array for each instrument, and each element of the array
# representing 24 units of time. each element of the array is either:
# a string "off" meaning the instrument isn't playing
# a string "on-off" meaning the instrument stops on that beat
# a string "on" meaning the instrument is playing
# a string "off-on" meaning the instrument starts on that beat

number_of_instruments = 12
playing = [False for i in range(number_of_instruments)]
timelines = [[] for i in range(number_of_instruments)]
instrument = 0
time = 0  # time attribute, in special units
last_fill = 0  # index of last fill of empty spots

for i, track in enumerate(midi.tracks):
    print('Track {}: {}'.format(i, track.name))
    for index, msg in enumerate(track):
        time += int(msg.time)
        if msg.is_meta:
            continue
        instrument = msg.note-36
        if msg.type == "note_off": 
            # fills in all spots until instrument state change
            for i in range(last_fill, int(time/24)): 
                timelines[instrument].append("on")
            timelines[instrument].append("on-off")
        elif msg.type == "note_on": 
            # fills in all spots until instrument state change
            for i in range(last_fill, int(time/24)):
                timelines[instrument].append("off")
            timelines[instrument].append("off-on")
        playing[instrument] = not playing[instrument]

        # if there aren't anymore instruments to change status of at
        # this time
        if track[index + 1].time != 0:
            for i in range(last_fill, int(time/24)+1):
                for j in range(len(playing)):
                    if playing[j] == True and len(timelines[j]) < (time/24):
                        timelines[j].append("on")
                    if playing[j] == False and len(timelines[j]) < (time/24):
                        timelines[j].append("off")
            last_fill = int(time/24) + 1 # update fill time

# from bottom to top: yeah, bell, big_synth, alarm, high_synth,
# background_vocals, ah_ah, snare, bass, bongo, spacey_synth, synth
for i in timelines:
    str = "::::: "
    for e in i[:20]:
        str += ''.join(format(e,'>8'))
    print(str)

# step 3: make a list of 'blocks', representing every possible 1/4 note
# segment (96 units of time). each block contains an array for each
# instrument, with each element a string (same definitions as above).
# each element of the array represents one of four subdivisions, or a
# 1/16 note. in addition, it should contain two dictionaries, each one
# containing possibles adjacencies and their probabilities before/after
# the block.

class Block:
    def __init__(
            self, name, yeah, bell, big_synth, alarm, high_synth,
            background_vocals, ah_ah, snare, bass, bongo, spacey_synth, synth,
            adjacencies1):
        self.id = name
        self.yeah = yeah
        self.bell = bell
        self.big_synth = big_synth
        self.alarm = alarm
        self.high_synth = high_synth
        self.background_vocals = background_vocals
        self.ah_ah = ah_ah
        self.snare = snare
        self.bass = bass
        self.bongo = bongo
        self.spacey_synth = spacey_synth
        self.synth = synth
        self.adjacencies1 = adjacencies1

    def is_equal(self, b):
        if (self.id == b.id and
            self.yeah == b.yeah and
            self.bell == b.bell and
            self.big_synth == b.big_synth and
            self.alarm == b.alarm and
            self.high_synth == b.high_synth and
            self.background_vocals == b.background_vocals and
            self.ah_ah == b.ah_ah and
            self.snare == b.snare and
            self.bass == b.bass and
            self.bongo == b.bongo and
            self.spacey_synth == b.spacey_synth and
            self.synth == b.synth):
            return True
        return False
