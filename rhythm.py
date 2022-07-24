import mido
import random
from copy import copy

# step 1: translating the midi file
# docs:
# https://mido.readthedocs.io/en/latest/messages.html#control-changes
midi = mido.MidiFile("input/3005.mid")
for i, track in enumerate(midi.tracks):
    print("Track {}: {}".format(i, track.name))
#     for msg in track:
#       print(msg)

# step 2: parse the MidiFile and translate to a structure we can use
number_of_instruments = 12
playing = [False for i in range(number_of_instruments)]
timelines = [[] for i in range(number_of_instruments)]
instrument = 0
time = 0  # time attribute, in special units
last_fill = 0  # index of last fill of empty spots

for i, track in enumerate(midi.tracks):
    for index, msg in enumerate(track):
        time += int(msg.time)
        if msg.is_meta:
            continue
        instrument = msg.note - 36
        if msg.type == "note_off":
            # fills in all spots until instrument state change
            for i in range(last_fill, int(time / 24)):
                timelines[instrument].append("on")
            timelines[instrument].append("on-off")
        elif msg.type == "note_on":
            # fills in all spots until instrument state change
            for i in range(last_fill, int(time / 24)):
                timelines[instrument].append("off")
            timelines[instrument].append("off-on")
        playing[instrument] = not playing[instrument]

        # if there aren't anymore instruments to change status of at
        # this time
        if track[index + 1].time != 0:
            for i in range(last_fill, int(time / 24) + 1):
                for j in range(len(playing)):
                    if playing[j] and len(timelines[j]) < (time / 24):
                        timelines[j].append("on")
                    if not playing[j] and len(timelines[j]) < (time / 24):
                        timelines[j].append("off")
            last_fill = int(time / 24) + 1  # update fill time

# from bottom to top: yeah, bell, big_synth, alarm, high_synth,
# background_vocals, ah_ah, snare, bass, bongo, spacey_synth, synth
# for i in timelines:
#     info = "::::: "
#     for e in i[:20]:
#         info += ''.join(format(e,'>8'))
#     print(info)

# step 3: make a list of 'blocks', representing every possible 1/4 note
# segment (96 units of time)
class Block:
    def __init__(
        self,
        name,
        synth,
        spacey_synth,
        bongo,
        bass,
        snare,
        ah_ah,
        background_vocals,
        high_synth,
        alarm,
        big_synth,
        bell,
        yeah,
        adjacencies1,
        adjacencies2,
    ):
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
        if (
            self.synth == b.synth
            and self.spacey_synth == b.spacey_synth
            and self.bongo == b.bongo
            and self.bass == b.bass
            and self.snare == b.snare
            and self.ah_ah == b.ah_ah
            and self.background_vocals == b.background_vocals
            and self.high_synth == b.high_synth
            and self.alarm == b.alarm
            and self.big_synth == b.big_synth
            and self.bell == b.bell
            and self.yeah == b.yeah
        ):
            return True
        return False


blocks = []
subdivisions_per_block = 4
id = 0
for i in range(int(len(timelines[0]) / subdivisions_per_block)):
    if i == 0:
        blocks.append(
            Block(
                id,
                timelines[0][i * 4 : (i + 1) * 4],
                timelines[1][i * 4 : (i + 1) * 4],
                timelines[2][i * 4 : (i + 1) * 4],
                timelines[3][i * 4 : (i + 1) * 4],
                timelines[4][i * 4 : (i + 1) * 4],
                timelines[5][i * 4 : (i + 1) * 4],
                timelines[6][i * 4 : (i + 1) * 4],
                timelines[7][i * 4 : (i + 1) * 4],
                timelines[8][i * 4 : (i + 1) * 4],
                timelines[9][i * 4 : (i + 1) * 4],
                timelines[10][i * 4 : (i + 1) * 4],
                timelines[11][i * 4 : (i + 1) * 4],
                {},
                {id + 1: 1},
            )
        )
        id += 1
    else:
        new_block = Block(
            id,
            timelines[0][i * 4 : (i + 1) * 4],
            timelines[1][i * 4 : (i + 1) * 4],
            timelines[2][i * 4 : (i + 1) * 4],
            timelines[3][i * 4 : (i + 1) * 4],
            timelines[4][i * 4 : (i + 1) * 4],
            timelines[5][i * 4 : (i + 1) * 4],
            timelines[6][i * 4 : (i + 1) * 4],
            timelines[7][i * 4 : (i + 1) * 4],
            timelines[8][i * 4 : (i + 1) * 4],
            timelines[9][i * 4 : (i + 1) * 4],
            timelines[10][i * 4 : (i + 1) * 4],
            timelines[11][i * 4 : (i + 1) * 4],
            {blocks[i - 1].id: 1},
            {},
        )
        add_to_id = True
        for b in blocks:
            if new_block == b:
                new_block.id = b.id
                add_to_id = False
                break
        blocks.append(new_block)
        blocks[i - 1].adjacencies2 = {new_block.id: 1}
        if add_to_id:
            id += 1


def addAdjacencies(a, b):
    adjacencies = a | b
    for key1, value1 in a.items():
        for key2, value2 in b.items():
            if key1 == key2:
                adjacencies[key1] = value1 + value2
    return adjacencies


blocks_no_repeats = []
for a in blocks:
    repeated = False
    for b in blocks_no_repeats:
        if a.id == b.id:
            b.adjacencies1 = addAdjacencies(a.adjacencies1, b.adjacencies1)
            b.adjacencies2 = addAdjacencies(a.adjacencies2, b.adjacencies2)
            repeated = True
    if not repeated:
        blocks_no_repeats.append(a)

# prints without repeats
# print("\n\n\n\n\n")
# for i in blocks_no_repeats:
#     print("*****", i.id, "*****")
#     print(vars(i))


class Tile:
    def __init__(self):
        self.possibilities = [
            [blocks_no_repeats[i], 0] for i in range(len(blocks_no_repeats))
        ]
        self.observed = False
        self.tile = None

    def observe(self):
        untouched = True
        for possibility in self.possibilities:
            if possibility[1] != 0:
                untouched = False
        if len(self.possibilities) > 0:
            if untouched:
                self.tile = random.choice(self.possibilities)[0]
            if not untouched:
                total = 0
                for possibility in self.possibilities:
                    total += possibility[1]
                choice = random.randint(0, total - 1)
                for possibility in self.possibilities:
                    if choice < possibility[1]:
                        self.tile = possibility[0]
                        break
                    else:
                        choice -= possibility[1]
            self.observed = True
        else:
            raise Exception("no possibilities")


generation_length = 100  # number of tiles in final product
tiles = [Tile() for i in range(generation_length)]

# using additive method of probability in this version, to create choices with greater success rate
def propagate(tiles, index, tracker):
    if index < 0 or index >= len(tiles) or tracker[index]:
        return
    last = index == len(tiles) - 1
    first = index == 0
    if first:  # just to avoid throwing error, inaccurate
        original_prev = copy(tiles[index].possibilities)
    else:
        original_prev = copy(tiles[index - 1].possibilities)
    if last:  # just to avoid throwing error, inaccurate
        original_next = copy(tiles[index].possibilities)
    else:
        original_next = copy(tiles[index + 1].possibilities)

    if tiles[index].observed:
        if not first:
            for possibility in tiles[index - 1].possibilities:
                if possibility[0].id in tiles[index].tile.adjacencies1:
                    possibility[1] += tiles[index].tile.adjacencies1[possibility[0].id]
                else:
                    possibility[1] = 0
        if not last:
            for possibility in tiles[index + 1].possibilities:
                if possibility[0].id in tiles[index].tile.adjacencies2:
                    possibility[1] += tiles[index].tile.adjacencies2[possibility[0].id]
                if not possibility[0].id in tiles[index].tile.adjacencies2:
                    possibility[1] = 0
    elif not tiles[index].observed:
        unobserved_adjacencies1 = {}
        unobserved_adjacencies2 = {}
        for possibility in tiles[index].possibilities:
            unobserved_adjacencies1 = addAdjacencies(
                unobserved_adjacencies1, possibility[0].adjacencies1
            )
            unobserved_adjacencies2 = addAdjacencies(
                unobserved_adjacencies2, possibility[0].adjacencies2
            )
        if not first:
            for possibility in tiles[index - 1].possibilities:
                if possibility[0].id in unobserved_adjacencies1:
                    possibility[1] += unobserved_adjacencies1[possibility[0].id]
                else:
                    possibility[1] = 0
        if not last:
            for possibility in tiles[index + 1].possibilities:
                if possibility[0].id in unobserved_adjacencies2:
                    possibility[1] += unobserved_adjacencies2[possibility[0].id]
                if not possibility[0].id in unobserved_adjacencies2:
                    possibility[1] = 0
    tracker[index] = True

    if not first and original_prev != tiles[index - 1].possibilities:
        propagate(tiles, index - 1, tracker)
    if not last and original_next != tiles[index + 1].possibilities:
        propagate(tiles, index + 1, tracker)
    return


def execute_wfc(tiles):
    complete = False
    while not complete:
        cont = False
        lowest_entropy = 0
        while tiles[lowest_entropy].observed:
            lowest_entropy += 1
        for i, tile in enumerate(tiles):
            if (
                len(tile.possibilities) < len(tiles[lowest_entropy].possibilities)
                and not tile.observed
            ):
                lowest_entropy = i
        try:
            tiles[lowest_entropy].observe()
        except Exception as e:
            tiles = [Tile() for i in range(generation_length)]
            print("restarting:", e)
            pass
        propagate(tiles, lowest_entropy, [False for i in range(len(tiles))])
        for tile in tiles:
            if not tile.observed:
                cont = True
        if not cont:
            complete = True


execute_wfc(tiles)

info = "\nlist of tiles: "
for tile in tiles:
    if tile is None:
        info += "None"
    else:
        info += str(tile.tile.id)
    info += "   "
print(info)
