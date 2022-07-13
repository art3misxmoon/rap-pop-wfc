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
            self, name, synth, spacey_synth, bongo, bass, snare, ah_ah,
            background_vocals, high_synth, alarm, big_synth, bell, yeah,
            adjacencies1, adjacencies2):
        self.id = name
        self.synth = synth
        self.spacey_synth = spacey_synth
        self.bongo = bongo
        self.bass = bass
        self.snare = snare
        self.ah_ah = ah_ah
        self.background_vocals = background_vocals
        self.high_synth = high_synth
        self.alarm = alarm
        self.big_synth = big_synth
        self.bell = bell
        self.yeah = yeah
        self.adjacencies1 = adjacencies1
        self.adjacencies2 = adjacencies2

    def __eq__(self, b):
        if (self.synth == b.synth and
            self.spacey_synth == b.spacey_synth and
            self.bongo == b.bongo and
            self.bass == b.bass and
            self.snare == b.snare and
            self.ah_ah == b.ah_ah and
            self.background_vocals == b.background_vocals and
            self.high_synth == b.high_synth and
            self.alarm == b.alarm and
            self.big_synth == b.big_synth and
            self.bell == b.bell and
            self.yeah == b.yeah):
            return True
        return False

Blocks = []
subdivisions_per_block = 4
for i in range(int(len(timelines[0])/subdivisions_per_block)):
    if i == 0:
        Blocks.append(Block(
            i, timelines[0][i*4:(i+1)*4], timelines[1][i*4:(i+1)*4],
            timelines[2][i*4:(i+1)*4], timelines[3][i*4:(i+1)*4],
            timelines[4][i*4:(i+1)*4], timelines[5][i*4:(i+1)*4],
            timelines[6][i*4:(i+1)*4], timelines[7][i*4:(i+1)*4],
            timelines[8][i*4:(i+1)*4], timelines[9][i*4:(i+1)*4],
            timelines[10][i*4:(i+1)*4], timelines[11][i*4:(i+1)*4],
            {}, {i+1: 1}))
    elif i > 0 and i < int(len(timelines[0])/subdivisions_per_block) - 1:
        Blocks.append(Block(
            i, timelines[0][i*4:(i+1)*4], timelines[1][i*4:(i+1)*4],
            timelines[2][i*4:(i+1)*4], timelines[3][i*4:(i+1)*4],
            timelines[4][i*4:(i+1)*4], timelines[5][i*4:(i+1)*4],
            timelines[6][i*4:(i+1)*4], timelines[7][i*4:(i+1)*4],
            timelines[8][i*4:(i+1)*4], timelines[9][i*4:(i+1)*4],
            timelines[10][i*4:(i+1)*4], timelines[11][i*4:(i+1)*4],
            {i-1: 1}, {i+1: 1}))
    elif i == int(len(timelines[0])/subdivisions_per_block) - 1:
        Blocks.append(Block(
            i, timelines[0][i*4:(i+1)*4], timelines[1][i*4:(i+1)*4],
            timelines[2][i*4:(i+1)*4], timelines[3][i*4:(i+1)*4],
            timelines[4][i*4:(i+1)*4], timelines[5][i*4:(i+1)*4],
            timelines[6][i*4:(i+1)*4], timelines[7][i*4:(i+1)*4],
            timelines[8][i*4:(i+1)*4], timelines[9][i*4:(i+1)*4],
            timelines[10][i*4:(i+1)*4], timelines[11][i*4:(i+1)*4],
            {i-1: 1}, {}))

# prints with repeats
for i in range(5): 
    print("*****", Blocks[i].id, "*****")
    print(vars(Blocks[i]))