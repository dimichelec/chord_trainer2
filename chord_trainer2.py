import random
import sys
import time

import config
import ui
import audio
import metronome
import chords


# process command line args and load config file
config = config.config()

# create a chords object
chords = chords.chords()

# setup the chord list we'll use
chord_chart = []
chord_sequence_index = 0
if config.chord_sequence != 0:
    for chord in chords.chord_sequences[config.chord_sequence-1]:
        chord_chart.append(chord)

# create the UI
ui = ui.ui(chords)

#  create and open the audio devices
audio = audio.audio(device_out=config.output_device)

# create the metronome
metronome = metronome.metronome(
    audio=audio, bpm=config.bpm, measures=config.chart_pos_max, chord_beats=config.chord_beats
)
audio.set_metronome(metronome)

# draw UI components
ui.draw_chord_box()
ui.draw_bpm(metronome.bpm,1)
if chord_chart != []:
    ui.draw_chart(chord_chart)

root = chord = position = ''

def get_random_chord():
    global root,chord,position
    root = chords.notes[int(random.random()*len(chords.notes))]
    chord = chords.formulas[int(random.random()*len(chords.formulas))][0]
    position = int(random.random()*3)+1


def get_list_chord():
    global root,chord,position,chord_chart,chord_sequence_index
    a = chord_chart[1:][chord_sequence_index]
    root = a[0]
    chord = a[1]
    position = int(a[2])


def next_list_chord_index():
    global chord_chart,chord_sequence_index
    return (0 if chord_sequence_index >= len(chord_chart)-2 else chord_sequence_index+1)


def draw_new_chord(new_chord=True):
    global root,chord,position
    global chord_chart,chord_sequence_index,show_diagram
    if chord_chart != []:
        chord_sequence_index = next_list_chord_index() if new_chord else 0
        get_list_chord()
        draw_chart_pointer()
    else:
        get_random_chord()
    ui.draw_chord(f'{root}{chord} - {position}', 1 if run else 0)
    if show_diagram:
        ui.draw_chart_diagram(root,chord,position)


def draw_chart_pointer():
    if config.chord_sequence != 0:
        ui.draw_chart_pointer(chord_sequence_index+1)


def init():
    global run,runtime,chord_sequence_index,chord_chart,first_beat

    # reset time and displays
    runtime = 0
    ui.draw_time(runtime)

    # reset metronome and displays
    metronome.reset()
    ui.draw_beatclock(1, 1)
    ui.draw_bpm(metronome.bpm, 1 if run else 0)

    # reset chord chart and displays
    draw_new_chord(False)

    # give initial chord full measure
    first_beat = True


run = False
show_diagram = True

init()

runtime_mark = time.perf_counter()
while True:

    # beat clock
    if run:
        if time.perf_counter() > (runtime_mark + 1):
            runtime += 1
            runtime_mark = time.perf_counter()
            ui.draw_time(runtime)
        state, measure, beat = metronome.service()
        if state > 0:
            if state == 1:
                beat_start = time.perf_counter()
                if first_beat:
                    first_beat = False
                else:
                    draw_new_chord()

            ui.draw_beatclock(measure, beat)

    # keystroke processing
    key = ui.keyhit().lower()

    if key == 'q':                          # quit app
        break
    elif key == '+':                        # BPM +1
        metronome.add(1)
        ui.draw_bpm(metronome.bpm, 1 if run else 0)
    elif key == '-':                        # BPM -1
        metronome.add(-1)
        ui.draw_bpm(metronome.bpm, 1 if run else 0)
    elif key == ' ':                        # start/stop metronome
        if run:
            run = False
        else:
            run = True
            beat_start = runtime_mark = time.perf_counter()
        ui.draw_bpm(metronome.bpm, 1 if run else 0)
        ui.draw_chord(f'{root}{chord} - {position}', 1 if run else 0)
    elif key == 'd':                        # hide/show chord diagram
        if show_diagram:
            ui.clear_chart_diagram()
            show_diagram = False
        else:
            ui.draw_chart_diagram(root,chord,position)
            show_diagram = True
    elif key == 'n':                        # draw next chord
        draw_new_chord()
        first_beat = True
    elif key == 'm':                        # mute/unmute metronome
        metronome.mute = False if metronome.mute else True
        ui.draw_mute(metronome.mute)
    elif key == 'r':                        # reset game
        run = False
        init()

    
ui.uninit()
audio.uninit()
sys.exit()

