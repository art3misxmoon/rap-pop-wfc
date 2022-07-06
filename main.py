import mido

midi = mido.MidiFile('3005.mid')

for i, track in enumerate(midi.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

