# rap-pop-wfc

## What is WFC? 

The [WaveFunctionCollapse (WFC) algorithm](https://github.com/mxgmn/WaveFunctionCollapse), created by Maxim Gumin, is an
example-driven generation algorithm that has been used initially in
image generation and further in applications such as 2D and 3D video
game level generation. The algorithm is powerful in creating cohesive
and near-infinite output based on constraint solving, and because of its
use of tile-like units, it may have significant applications in music
and lyric generation. Previously, WFC has been applied in: 

- Alice in Wonderland-inspired sonnet generation in [Martin O’Leary’s
Oisín project](https://github.com/mewo2/oisin/tree/0e391d6dbbf931c2257a7625682a26b25733b25c).
- [the Piano Teacher game](https://creativecoding.soe.ucsc.edu/courses/cmpm202_w20/_schedule/Pettitt_202.pdf) created by Jared Pettitt, Celeste C. Jewett,
and Tamara Duplantis to generate example pieces for learning pianists. 

##Our Research

In our research, we applied WFC to both MIDI beat and lyric generation,
specifically generating contemporary hip-hop music based on input from
Donald Glover’s, professionally known as Childish Gambino’s, studio
album Because the Internet. We created two different WFC generation
models using Python and Ableton Live as a MIDI editor: the beat
generation in ```rhythm.py``` is an original creation, using input MIDI
files sequenced from Childish Gambino’s music; the lyric generation is a
modified version of Oisín, using metric patterns from the input corpus.

We created successful output in each generation model with similar
characteristics to the input, that can further be improved and examined
by combining the lyrics and beats together into complete songs. This
research demonstrates the potential of WaveFunctionCollapse in driving
forward the field of genre-specific, example-based music generation. 
