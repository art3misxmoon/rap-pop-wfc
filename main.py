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
# 1 array for each instrument, and each element of the array representing 12 units of time. 
# each element of the array is either:
# a string "off" meaning the instrument isn't playing
# a string "on-off" meaning the instrument stops on that beat
# a string "on" meaning the instrumnt is playing
# a string "off-on" meaning the instrument starts on that beat

# step 3: make a list of 'blocks', representing every possible 1/4 note segment (16 units of time)
# each block contains a two-item array for each instrument, with each element a string (same definitions as above)
# each element of the array represents one of two subdivisions, or an 1/8 note