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
chord_list = []
chord_sequence_index = 0
if config.chord_sequence != 0:
    for chord in chords.chord_sequences[config.chord_sequence-1]:
        chord_list.append(chord)

# create the UI
ui = ui.ui(chords)

#  create and open the audio devices
audio = audio.audio(device_out = config.output_device)

# create the metronome
metronome = metronome.metronome(
    audio=audio, bpm=config.bpm, measures=config.chart_pos_max, chord_beats=config.chord_beats
)
audio.set_metronome(metronome)


# draw UI components
ui.draw_chord_box()
ui.draw_bpm(metronome.bpm)
ui.draw_sequence_name("Sequence: " + ("Random" if config.chord_sequence == 0 else chord_list[0]))


def get_random_chord():
    return (
        chords.notes[int(random.random()*len(chords.notes))],
        chords.formulas[int(random.random()*len(chords.formulas))][0],
        int(random.random()*3)+1
    )


def get_list_chord():
    global chord_list,chord_sequence_index
    chord = chord_list[chord_sequence_index+1]
    chord_sequence_index = 0 if chord_sequence_index == len(chord_list)-2 else chord_sequence_index + 1
    return (chord[0], chord[1], int(chord[2]))


def draw_next_chord(show_diagram):
    if config.chord_sequence == 0:
        root, chord, position = get_random_chord()
    else:
        root, chord, position = get_list_chord()
    ui.draw_chord(f'{root}{chord} - {position}', 1)
    if show_diagram:
        ui.draw_chart_diagram(root,chord,position)
    return (root, chord, position)


run = True
measure = 1
show_diagram = True
chord_count = 0

runtime_mark = time.perf_counter()
runtime = 0

while True:

    # beat clock
    if run:
        if (time.perf_counter() - runtime_mark) >= 1.:
            runtime += 1
            runtime_mark += 1.
            ui.draw_timecount(f'{runtime//3600:01d}:{runtime//60:02d}:{runtime%60:02d}', chord_count)
        state, measure, beat = metronome.service()
        if state > 0:
            if state == 1:
                beat_start = time.perf_counter()
                (root, chord, position) = draw_next_chord(show_diagram)
                chord_count += 1

            ui.draw_beatclock(measure, beat)

    # keystroke processing
    key = ui.keyhit().lower()
    if key == 'q':                          # quit app
        break
    elif key == '+':                        # BPM +1
        metronome.add(1)
        ui.draw_bpm(metronome.bpm)
    elif key == '-':                        # BPM -1
        metronome.add(-1)
        ui.draw_bpm(metronome.bpm)
    elif key == ' ':                        # start/stop metronome
        if run:
            run = False
        else:
            run = True
            beat_start = runtime_mark = time.perf_counter()
    elif key == 'd':                        # hide/show chord diagram
        if show_diagram:
            ui.clear_chart_diagram()
            show_diagram = False
        else:
            ui.draw_chart_diagram(root,chord,position)
            show_diagram = True
    elif key == 'n':                        # draw next chord
        draw_next_chord(show_diagram)
    elif key == 'm':                        # mute/unmute metronome
        metronome.mute = False if metronome.mute else True
        ui.draw_mute(metronome.mute)

    # elif key == 'r':                        # reset game
    #     metronome.reset()
    #     game.reset()

    
ui.uninit()
audio.uninit()
sys.exit()

