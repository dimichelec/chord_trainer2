import random
import sys
import time

import config
import ui
import audio
import metronome


# process command line args and load config file
config = config.config()

# create the UI
ui = ui.ui()

#  create and open the audio devices
audio = audio.audio(device_out = config.output_device)

# create the metronome
metronome = metronome.metronome(
    audio=audio, bpm=config.bpm, measures=config.chart_pos_max, chord_beats=config.chord_beats
)
audio.set_metronome(metronome)

roots = ['C','C#','Db','D','D#','Eb','E','F','F#','Gb','G','G#','Ab','A','A#','Bb','B']
chords = ['M7','m7','7','m7b5','M9','m9','9','M11','m11','11']
positions = ['root 1','root 2','root 3']

chord_list = [('G','M7','1'), ('C','M7','2'), ('F','M7','3'), ('G','M7','3'), ('D','M7','2'), ('A','M7','1')]
chord_list_index = 0

# draw UI components
ui.draw_chord_box()
ui.draw_bpm(metronome.bpm)


run = True
measure = 1


def get_random_chord():
    global roots, chords, positions
    return (roots[int(random.random()*len(roots))],
        chords[int(random.random()*len(chords))],
        positions[int(random.random()*len(positions))]
    )


def get_list_chord():
    global chord_list, chord_list_index
    root, chord, position = chord_list[chord_list_index]
    chord_list_index = 0 if chord_list_index == len(chord_list)-1 else chord_list_index + 1
    return (root, chord, position)


def draw_next_chord():
    global chord_list, chord_list_index

    root, chord, position = get_random_chord()
    # root, chord, position = get_list_chord()

    ui.draw_chord(f'{root}{chord} - {position[-1]}', 1)
    ui.draw_chart_diagram(root,chord,int(position[-1]))


while True:

    # beat clock
    if run:
        state, measure, beat = metronome.service()
        if state > 0:
            if state == 1:
                beat_start = time.perf_counter()
                draw_next_chord()

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
        run = True if not run else False
    elif key == 'n':                        # draw next chord
        draw_next_chord()

    # elif key == 'r':                        # reset game
    #     metronome.reset()
    #     game.reset()

    
ui.uninit()
audio.uninit()
sys.exit()

