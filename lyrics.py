import sys
from tokenize import String
from oisin import oisin

filename = "input/lyrics.txt"
try:
    filename = sys.argv[1]
except IndexError:
    pass

tripletrhythmcouplet = [ oisin.Line([('-', '.', '.', '.', '.', '.', '-', '.', '.')], 'a' ), oisin.Line([('-', '.', '.', '.', '.', '-', '.', '.')], 'a' ) ]

line = ". / . . / . . / / ."
# produces a line of verse with dictated word stress
# @param word stress patterm  ex: "/ . . . / . ."
def rhythmLine(line, rhyme):
    lineWithoutSpaces = ""
    x = 0
    while True:
        if line[x] == '/':
           lineWithoutSpaces += '-'
        else:
            lineWithoutSpaces += '.'
        x += 2
        if (x > len(line)):
            break

    elements = tuple(lineWithoutSpaces)
    return oisin.Line([elements], rhyme)

oisin.balladize(
    oisin.load(filename), meter=[rhythmLine(line, 'a'), rhythmLine(line, 'b'), rhythmLine(line, 'a')], step=50, order=2
)
