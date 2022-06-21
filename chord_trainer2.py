import sys
import time

import config
import chords
import audio
import metronome
import ui


# process command line args and load config file
config = config.config()

# setup the chords
chords = chords.chords()
current_chord = None
chord_chart = []
chord_sequence_index = 0

# chord format from sequences is {A-G}[b/#][m/M][2-13][b/#][2-13][-][1-3]
if config.chord_sequence != 0:
    chord_chart.append(chords.chord_sequences[config.chord_sequence-1][0])
    for chord in chords.chord_sequences[config.chord_sequence-1][1:]:
        position = 0
        try:
            i = chord.index('-')
            position = int(chord[i+1:])
            chord = chord[:i]
        except:
            pass

        print(chord,position)

        root = chord[0]
        if (chord[1]=='#') or (chord[1]=='b'):
            root += chord[1]
            type = chord[2:]
        else:
            type = chord[1:]

        chord_chart.append((root,type,position))


#  create and open the audio devices and metronome
audio = audio.audio(device_out=config.output_device)
metronome = metronome.metronome(
    audio=audio, bpm=config.bpm, measures=config.chart_pos_max, chord_beats=config.chord_beats
)
audio.set_metronome(metronome)

# create UI and draw components
ui = ui.ui(chords)
ui.draw_chord_box()
ui.draw_bpm(metronome.bpm,1)
if chord_chart != []:
    ui.draw_chart(chord_chart)


def draw_new_chord(reset=False):
    global current_chord
    global chord_chart,chord_sequence_index,show_diagram
    if chord_chart != []:
        chord_sequence_index = 0 if reset or (chord_sequence_index >= (len(chord_chart)-2)) else (chord_sequence_index+1)
        current_chord = chord_chart[1:][chord_sequence_index]
        ui.draw_chart_pointer(chord_sequence_index+1)
    else:
        current_chord = chords.get_random_chord()
    ui.draw_chord(current_chord, 1 if run else 0)
    if show_diagram:
        ui.draw_chart_diagram(current_chord)


def init():
    global run,runtime,first_beat

    # reset time and displays
    runtime = 0
    ui.draw_time(runtime)

    # reset metronome and displays
    metronome.reset()
    ui.draw_beatclock(1, 1)
    ui.draw_bpm(metronome.bpm, 1 if run else 0)

    # reset chord chart and displays
    draw_new_chord(reset=True)

    # give initial chord full measure
    first_beat = True


def keystroke_service():
    global run,show_diagram,first_beat,beat_start,runtime_mark

    # keystroke processing
    key = ui.keyhit().lower()

    # quit app
    if key == 'q':
        return False
    
    # BPM +1
    elif key == '+':
        metronome.add(1)
        ui.draw_bpm(metronome.bpm, 1 if run else 0)

    # BPM -1
    elif key == '-':
        metronome.add(-1)
        ui.draw_bpm(metronome.bpm, 1 if run else 0)

    # start/stop metronome
    elif key == ' ':
        run = False if run else True
        if run:
            beat_start = runtime_mark = time.perf_counter()
        ui.draw_bpm(metronome.bpm, 1 if run else 0)
        ui.draw_chord(current_chord, 1 if run else 0)

    # hide/show chord diagram
    elif key == 'd':
        if show_diagram:
            ui.clear_chart_diagram()
            show_diagram = False
        else:
            ui.draw_chart_diagram(current_chord)
            show_diagram = True

    # draw next chord
    elif key == 'n':
        draw_new_chord()
        first_beat = True

    # mute/unmute metronome
    elif key == 'm':
        metronome.mute = False if metronome.mute else True
        ui.draw_mute(metronome.mute)

    # reset
    elif key == 'r':
        run = False
        init()

    # return normally
    return True


run = False
show_diagram = True

init()

runtime_mark = time.perf_counter()
while True:

    # beat clock
    if run:
        if time.perf_counter() > (runtime_mark + 1):
            runtime += 1
            runtime_mark += 1
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

    # process keystrokes and exit while loop if user requests it
    if not keystroke_service():
        break


# uninitialize stuff before exiting    
ui.uninit()
audio.uninit()
sys.exit()

