
import msvcrt
import pyfiglet
import cursor

from colorama import Fore, Back, Style
from colorama import init


class ui:

    # sequence name ------------------------------------------------------
    def draw_sequence_name(self,name):
        print(f'\033[2;3H'
            + Style.DIM + Fore.WHITE + Back.BLACK
            + f'{name}')

    # beatclock ----------------------------------------------------------
    def draw_beatclock(self,measure,beat):
        print(f'\033[2;39H'
            + Style.BRIGHT + Fore.WHITE + Back.BLACK
            + f'{measure}:{beat}')

    # signal indicator ---------------------------------------------------
    signal_on   = Style.BRIGHT + Fore.RED + Back.BLACK + '▀'  #'■'
    signal_off  = Style.DIM    + Fore.RED + Back.BLACK + ' '  #'□'

    def draw_signal(self,signal):
        print(f'\033[4;4H' + (self.signal_on if signal else self.signal_off))

    # mute indicator -----------------------------------------------------
    def draw_mute(self,mute):
        print(f'\033[2;66H' + Style.DIM + Fore.RED + Back.BLACK
            + ("MUTE" if mute else "    "))

    # bpm ----------------------------------------------------------------
    def draw_bpm(self,bpm):
        print(f'\033[2;71H' + Style.DIM + Fore.GREEN + Back.BLACK
            + f'{bpm:3d} BPM')

    # chord box ----------------------------------------------------------
    chord_top       = 3
    chord_left      = 2
    chord_width     = 75
    chord_height    = 7
    chord_box_style = Style.DIM + Fore.BLUE + Back.BLACK

    def draw_chord_box(self):
        y = self.chord_top
        print(f'\033[{y};{self.chord_left}H'
                + self.chord_box_style + '┌' + self.chord_width*'─' + '┐')
        y += 1
        for i in range(self.chord_height):
            print(f'\033[{y};{self.chord_left}H'
                + self.chord_box_style + '|' + self.chord_width*' ' + '|')
            y += 1
        print(f'\033[{y};{self.chord_left}H'
            + self.chord_box_style + '└' + self.chord_width*'─' + '┘')

    # chord --------------------------------------------------------------
    chord_styles = [
        Style.DIM    + Fore.WHITE + Back.BLACK,
        Style.BRIGHT + Fore.GREEN + Back.BLACK,
        Style.BRIGHT + Fore.RED   + Back.BLACK,
        Style.BRIGHT + Fore.WHITE + Back.BLACK
    ]

    def draw_chord(self,chord,style):
        fig = pyfiglet.figlet_format(chord,font='slant')
        fs = fig.splitlines()
        y = self.chord_top + 1
        pad = (self.chord_width - len(fs[0])) // 2
        for line in fs:
            print(f'\033[{y};{self.chord_left + 1}H'
                + self.chord_styles[style]
                + pad*' ' + line + pad*' ')
            y += 1


    # timer/counter ------------------------------------------------------
    timecount_top  = chord_top + chord_height + 2
    timecount_left = chord_left + 1

    def draw_timecount(self,time,count):
        print(f'\033[{self.timecount_top};{self.timecount_left}H'
            + Style.BRIGHT + Fore.WHITE + Back.BLACK
            + f'{time}/{count} chords')


    # chord score --------------------------------------------------------
    chord_score_top  = chord_top + chord_height
    chord_score_left = chord_left + 3

    def draw_chord_score(self,score):
        x = self.chord_score_left + ((self.chord_width - 4) - len(score))//2
        print(f'\033[{self.chord_score_top};{x}H{score}     ')


    # chord chart --------------------------------------------------------
    chart_top           = 12
    chart_left          = 4
    chart_style         = Style.BRIGHT + Fore.WHITE + Back.BLACK
    chart_positions     = []

    def draw_chart(self,chart):
        a = ''
        x = 0
        chart_positions = []
        for chord in chart:
            b = chord[0]
            if chord[1] == 'min':
                b += 'm'
            elif chord[1] == 'dim':
                b += '°'
            self.chart_positions.append(x)
            x += len(b) + 2
            a += b + '  '

        print(f'\033[{self.chart_top};{self.chart_left}H'
            + self.chart_style + a)

    # chord chart pointer ------------------------------------------------
    chart_pointer_on        = Style.BRIGHT + Fore.YELLOW + Back.BLACK + '▲'
    chart_pointer_off       = Style.BRIGHT + Fore.YELLOW + Back.BLACK + ' '
    last_chart_pointer_loc  = 0

    def draw_chart_pointer(self,measure):
        if self.last_chart_pointer_loc > 0:
            print('\033['
                + f'{self.chart_top+1};{self.last_chart_pointer_loc}H'
                + self.chart_pointer_off)
        if measure > 0:
            self.last_chart_pointer_loc = self.chart_left + self.chart_positions[measure-1]
            print('\033['
                + f'{self.chart_top+1};{self.last_chart_pointer_loc}H'
                + self.chart_pointer_on)

    # chord diagram ------------------------------------------------------
    diagram_top       = 2
    diagram_left      = 83
    diagram_height    = 15
    diagram_width     = 29

    def draw_chart_diagram(self,root,type,chord_form=0):
        y = self.diagram_top
        for line in self.chords.diagram(root,type,chord_form):
            print(f'\033[{y};{self.diagram_left}H{line}')
            y += 1
        while y <= self.diagram_height:
            print(f'\033[{y};{self.diagram_left}H' + (self.diagram_width*' '))
            y += 1

    def clear_chart_diagram(self):
        y = self.diagram_top
        for line in range(self.diagram_height):
            print(f'\033[{y};{self.diagram_left}H' + (self.diagram_width*' '))
            y += 1


    # stats lines --------------------------------------------------------
    stats_top       = chart_top + 3
    stats_left      = chart_left
    stats_style     = Style.DIM + Fore.CYAN + Back.BLACK
    stats_style1    = Style.BRIGHT + Fore.CYAN + Back.BLACK

    def draw_stats_line(self,line,stat):
        print(f'\033[{self.stats_top+line};{self.stats_left}H'
            + self.stats_style + stat)


    # help lines ---------------------------------------------------------
    help_top        = 14
    help_left       = chart_left
    help_column2    = chart_left + 40
    help_bottom     = 20

    def draw_help(self):
        y = self.help_top
        x = self.help_left
        print(f'\033[{y};{x}H'  + Fore.LIGHTBLACK_EX + '<space>  start/stop metronome');  y += 1
        print(f'\033[{y};{x}H'  + Fore.LIGHTBLACK_EX + '  +/-    change BPM');            y += 1
        print(f'\033[{y};{x}H'  + Fore.LIGHTBLACK_EX + '   M     mute/unmute metronome'); y += 1
        
        y = self.help_top
        x = self.help_column2
        print(f'\033[{y};{x}H' + Fore.LIGHTBLACK_EX + 'N  skip to next chord');      y += 1
        print(f'\033[{y};{x}H' + Fore.LIGHTBLACK_EX + 'D  hide/show chord diagram'); y += 1

        print(f'\033[{self.help_bottom};{self.help_left}H' + Fore.LIGHTBLACK_EX + 'Hit <Q> to exit')


    def keyhit(self):
        key = ''
        if msvcrt.kbhit():
            key = msvcrt.getch()
            key = chr(key[0])
        return key


    def __init__(self,chords):

        # styles
        self.default_style = Style.RESET_ALL
        self.chords = chords

        # init the display
        init()              # init colorama
        cursor.hide()
        print('\033[2J')    # clear screen
        self.draw_help()

        # draw a box for the chord display
        self.draw_chord_box()
        self.draw_signal(False)


    def uninit(self):
        print(Style.RESET_ALL + '\033[20;1H')
        cursor.show()

