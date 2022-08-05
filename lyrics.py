import sys
from tokenize import String
from oisin import oisin

filename = "input/lyrics.txt"
try:
    filename = sys.argv[1]
except IndexError:
    pass

tripletrhythmcouplet = [ oisin.Line([('-', '.', '.', '.', '.', '.', '-', '.', '.')], 'a' ), oisin.Line([('-', '.', '.', '.', '.', '-', '.', '.')], 'a' ) ]

verse1 = [". / . . . / . . . /", ". . . / . / . . . /", "/ . / . / . / . / . . /", "/ . / . . / / ."]
verse2 = ["/ . / . / . / . . / . . / / .", "/ . . / . . / . / . / . .", ". . / . . / . / . . /", "/ . / . / . / . . . / . . / /", "/ . / . /"]
verse3 = ["/ . / . . / . . / .", "/ / . / / . / / . . / .", ". . / . / / . / . / . . / .", "/ . / . . / . . . / . . / .", ". . / . . / . . / . / . . / .", "/ . . / . . / . . . . / . . / ."]
verse4 = [". / . / . . / / . / . . / . .", " . . / . . / . . . / . . / . ."]
verse5 = ["/ . . . . . / . .", "/ . . . . / . .", "/ . . . . / . .", "/ . . . . / . .", "/ . . . / . . / ."]
verse6 = [". / . . . / . /", ". / . . /", "/ / . . . . . . / . .", ". / . . . . / . . / . / .", ". / . . / . . . . / .", ". / . . / . / ."]
verse7 = [". / . . / .", ". / . . / .", ". / . . / .", ". / . . / ."]
verse8 = [". / . / . / / . . / . / .", ". / . . / . . / . . / .", "/ . . / .", ". / . . / . . / ."]


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

def createVerse(arrayOfLines):
    rhythm = []
    x = 0
    while True:
        rhythm.append(rhythmLine(arrayOfLines[x], 'a'))
        x += 1
        if x >= len(arrayOfLines):
            break;
    return rhythm


oisin.balladize(
    oisin.load(filename), meter=createVerse(verse8), step=50, order=2
)

