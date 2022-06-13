import random
import sys
import time
import msvcrt
import pyfiglet
import cursor
from colorama import Fore, Back, Style
from colorama import init

import metronome
import audio
import config

chart_pos_max = 1
chord_beats = 4


# process command line args and load config file
config = config.config()

# create the metronome
metronome = metronome.metronome(
    audio, bpm=config.bpm, measures=chart_pos_max, chord_beats=chord_beats)
audio.set_metronome(metronome)


roots = ['C','C#','Db','D','D#','Eb','E','F','F#','Gb','G','G#','Ab','A','A#','Bb','B']
chords = ['maj7','min7','dom7','min7b5']
positions = ['root 1','root 2','root 3']


# chord box ----------------------------------------------------------
chord_top       = 3
chord_left      = 2
chord_width     = 75
chord_height    = 7
chord_box_style = Style.DIM + Fore.BLUE + Back.BLACK

def draw_chord_box():
    global chord_top, chord_left, chord_box_style, chord_width, chord_height
    y = chord_top
    print(f'\033[{y};{chord_left}H'
            + chord_box_style + '┌' + chord_width*'─' + '┐')
    y += 1
    for i in range(chord_height):
        print(f'\033[{y};{chord_left}H'
            + chord_box_style + '|' + chord_width*' ' + '|')
        y += 1
    print(f'\033[{y};{chord_left}H'
        + chord_box_style + '└' + chord_width*'─' + '┘')


# beatclock ----------------------------------------------------------
def draw_beatclock(measure,beat):
    print(f'\033[2;32H'
        + Style.BRIGHT + Fore.WHITE + Back.BLACK
        + f'{measure}:{beat}')

# bpm ----------------------------------------------------------------
def draw_bpm(bpm):
    print(f'\033[2;56H' + Style.DIM + Fore.GREEN + Back.BLACK
        + f'{bpm:3d} BPM')

# chord --------------------------------------------------------------
chord_styles = [
    Style.DIM    + Fore.WHITE + Back.BLACK,
    Style.BRIGHT + Fore.GREEN + Back.BLACK,
    Style.BRIGHT + Fore.RED   + Back.BLACK,
    Style.BRIGHT + Fore.WHITE + Back.BLACK
]

def draw_chord(chord,style):
    global chord_top, chord_width, chord_styles, chord_left
    #fig = pyfiglet.figlet_format(f'{chord[0]} {chord[1]}', font='slant')
    fig = pyfiglet.figlet_format(chord,font='slant')
    fs = fig.splitlines()
    y = chord_top + 1
    pad = (chord_width - len(fs[0])) // 2
    for line in fs:
        print(f'\033[{y};{chord_left + 1}H'
            + chord_styles[style]
            + pad*' ' + line + pad*' ')
        y += 1


def keyhit():
    key = ''
    if msvcrt.kbhit():
        key = msvcrt.getch()
        key = chr(key[0])
    return key


tempo = 30

# styles
default_style = Style.RESET_ALL

# init the display
init()              # init colorama
cursor.hide()
print('\033[2J')    # clear screen
print('\033[20;2H' + Fore.LIGHTBLACK_EX + 'Hit <Q> to exit')

draw_chord_box()
draw_bpm(tempo)

runflag = True

chords = ['maj7']

last_T = time.perf_counter()

while runflag:
    root = roots[int(random.random()*len(roots))]
    chord = chords[int(random.random()*len(chords))]
    position = positions[int(random.random()*len(positions))]
    fig = pyfiglet.figlet_format(f'{root}{chord} - {position[-1]}', font='slant')
    draw_chord(f'{root}{chord} - {position[-1]}', 1)
    T = 60./(tempo/4.)

    while (time.perf_counter() - last_T) < T:
        # keystroke processing
        key = keyhit()
        if key == 'q':                          # quit app
            runflag = False
            break
        # elif key == '+':                        # BPM +1
        #     metronome.add(1)
        #     ui.draw_bpm(metronome.bpm)
        # elif key == '-':                        # BPM -1
        #     metronome.add(-1)
        #     ui.draw_bpm(metronome.bpm)
        # elif key == ' ':                        # start/stop metronome
        #     run = True if not run else False
        # elif key == 'r':                        # reset game
        #     metronome.reset()
        #     game.reset()
        #     lead_in = 4
    
    last_T = time.perf_counter()

print(Style.RESET_ALL + '\033[20;1H')
cursor.show()

sys.exit()

