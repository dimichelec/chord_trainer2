
import random


class chords:

    chart_maj = [
        [ ('C','maj'), ('D','min'), ('E','min'), ('F','maj'), ('G','maj'), ('A','min'), ('B','dim') ]
    ]

    # the standard tuning 3 bass strings of a guitar
    bass_tuning = ('E','A','D')
    notes = ('C','C#','D','D#','E','F','F#','G','G#','A','A#','B')

    # (chord type <M = major, m = minor> [
    #   The following pattens are in order from root note on low E string, A string...
    #   (fret pattern by string, low E first, -1 = don't play, 0 = play open),
    #   (interval of fretted strings from root, 0 = string not played, 1 = root)
    # ])
    #
    # Here's a good online chord DB: https://chords.gock.net/

    formulas = [
        ('M7', [
            (( 0,-1,1,1,0,-1), (1,0,7,3,5,0)),       # root on low E string
            ((-1, 0,2,1,2, 0), (0,1,5,7,3,5)),       # root on A string
            ((-1,-1,0,2,2, 2), (0,0,1,5,7,3))]),     # root on D string
        ('7', [
            (( 0,-1,0,1,0,-1), (1,0,-7, 3, 5,0)),     # root on low E string
            ((-1, 2,1,2,0,-1), (0,1, 3,-7, 1,0)),     # root on A string
            ((-1,-1,0,2,1, 2), (0,0, 1, 5,-7,3))]),   # root on D string
        ('m7', [
            ((0,-1,0,0,0,-1), (1,0,-7,-3, 5, 0)),     # root on low E string
            ((-1,0,2,0,1,-1), (0,1, 5,-7,-3, 0)),     # root on A string
            ((-1,-1,0,2,1,1), (0,0, 1, 5,-7,-3))]),   # root on D string
        ('m7b5', [
            (( 1,-1,1,1,0,-1), (1,0,-7,-3,-5, 0)),    # root on low E string
            ((-1, 0,1,0,1,-1), (0,1,-5,-7,-3, 0)),    # root on A string
            ((-1,-1,0,1,1, 1), (0,0, 1,-5,-7,-3))]),  # root on D string
        ('M9', [
            (( 1, 0,2,0,-1,-1), (1,3,7,9,0,0)),       # root on low E string
            ((-1, 1,0,2, 1,-1), (0,1,3,7,9,0)),       # root on A string
            ((-1,-1,1,0, 3, 1), (0,0,1,3,7,9))]),     # root on D string
        ('9', [
            (( 3,-1,3,2,0,-1), (1,0,-7, 9, 3, 0)),    # root on low E string
            ((-1, 1,0,1,1, 1), (0,1, 3,-7, 9, 5)),    # root on A string
            ((-1,-1,1,0,2, 1), (0,0, 1, 3,-7, 9))]),  # root on D string
        ('m9', [
            (( 2, 0,2,1,-1,-1), (1,-3,-7, 9, 0,0)),   # root on low E string
            ((-1, 2,0,2, 2,-1), (0, 1,-3,-7, 9,0)),   # root on A string
            ((-1,-1,2,0, 3, 2), (0, 0, 1,-3,-7,9))]), # root on D string
        ('M11', [
            (( 2,-1, 3,1, 0,-1), (1,0,7,9,11, 0)),    # root on low E string
            ((-1, 2,-1,3, 2, 0), (0,1,0,7, 9,11)),    # root on A string
            ((-1,-1, 4,3, 0, 1), (0,0,1,3,11, 7))]),  # root on D string
        ('11', [
            (( 2,-1,2,3,0,-1), (1,0,-7, 3,11, 0)),    # root on low E string
            ((-1, 2,1,2,0, 0), (0,1, 3,-7, 1,11)),    # root on A string
            ((-1,-1,4,3,0, 0), (0,0, 1, 3,11,-7))]),  # root on D string
        ('m11', [
            (( 2,-1, 2,2, 0,-1), (1,0,-7,-3,11, 0)),    # root on low E string
            ((-1, 2,-1,2, 3, 0), (0,1, 0,-7,-3,11)),    # root on A string
            ((-1,-1, 0,0, 1, 1), (0,0, 1,11,-7,-3))]),  # root on D string
    ]


    chord_sequences = [
        ["Major 7s",           'GM7-1','CM7-2','FM7-3','GM7-3','DM7-2','AM7-1'],
        ["Minor 7s",           'Gm7-1','Cm7-2','Fm7-3','Gm7-3','Dm7-2','Am7-1'],
        ["Dominant 7s",        'G7-1', 'C7-2', 'F7-3', 'G7-3', 'D7-2', 'A7-1' ],
        ["Major 9s",           'GM9-1','CM9-2','FM9-3','GM9-3','DM9-2','AM9-1'],
        ["Minor 9s",           'Gm9-1','Cm9-2','Fm9-3','Gm9-3','Dm9-2','Am9-1'],
        ["Dominant 9s",        'G9-1', 'C9-2', 'F9-3', 'G9-3', 'D9-2', 'A9-1' ],
        ["Gmaj ii-V-I",        'Am7-1','D7-2', 'GM7-1'],
        ["C F Bb ii-V-Is",     'Dm7', 'G7', 'CM7',  'Gm7', 'C7', 'FM7',  'Cm7', 'F7', 'BbM7'],
        ["Eb Ab Db ii-V-Is",   'Fm7', 'Bb7','EbM7', 'Bbm7','Eb7','AbM7', 'Ebm7','Ab7','DbM7'],
        ["Gb B E ii-V-Is",     'Abm7','Db7','GbM7', 'C#m7','F#7','BM7',  'F#m7','B7', 'EM7' ],
        ["A D G ii-V-Is",      'Bm7', 'E7', 'AM7',  'Em7', 'A7', 'DM7',  'Am7', 'D7', 'GM7' ],
    ]


    # given the root note and chord type, return a chord from our formulas played
    # in lowest neck position
    def find_best_chord(self,root,type,chord_form=0):

        # find the forms for the chord type
        forms = list(filter(lambda x: x[0] == type, self.formulas))[0][1]

        # find the note index of the root note
        try:
            iroot = self.notes.index(root)
        except ValueError:
            iroot = self.notes.index(root[0])-1 if ('-' in root) or ('b' in root) else iroot
            iroot += len(self.notes) if iroot < 0 else 0

        if chord_form == 0:
            # find the form that will fit in the lowest position on the neck, based on
            # which string our root note will be on.
            # returns tuple (root string, root fret, chord form, string intervals)
            out = ()
            root_string = root_fret = iform = 0
            for open_note in self.bass_tuning:
                iopen = self.notes.index(open_note)
                root_fret = (iroot - iopen) if (iroot >= iopen) else (12 + iroot - iopen)
                try:
                    if forms[iform][1][root_string] == 1:
                        form = forms[iform]
                        if root_fret < form[0][root_string]:
                            root_fret += 12
                        if (out == ()) or (root_fret < out[1]):
                            out = (root_string, root_fret, form[0], form[1])
                        iform += 1
                except:
                    pass
                root_string += 1
        else:
            # chord_form is not zero, use prescribed chord_form
            iopen = self.notes.index(self.bass_tuning[chord_form-1])
            root_fret = (iroot - iopen) if (iroot >= iopen) else (12 + iroot - iopen)
            form = forms[chord_form-1]
            if root_fret < form[0][chord_form-1]:
                root_fret += 12
            out = (chord_form-1, root_fret, form[0], form[1])

        return out


    def diagram(self,root,type,chord_form=0):
        out = []
        chord = self.find_best_chord(root,type,chord_form)
        root_string = chord[0]
        root_fret = chord[1]
        form = chord[2]
        intervals = chord[3]
        MAX_FRETS = 5


        def interval_ascii(i):
            b = 'R' if i == 1 else str(abs(i))
            a = 'p' if i in (4,5,11) else ' '
            a = 'b' if i < 0 else a
            if abs(i) in (1,3,5):
                return f'\033[41;1m{a}{b} \033[0m'
            elif abs(i) in (11,13):
                return f'\033[30;47m{a}{b}\033[0m'
            else:
                return f'\033[30;47m{a}{b} \033[0m'


        def position_ascii(position):
            out = 'th'
            if position == 1:
                out = 'st'
            elif position == 2:
                out = 'nd'
            elif position == 3:
                out = 'rd'
            return str(position) + out

        out.append(f'\033[37;1m{root}{type} -{root_string+1}\033[0m     ')

        fret_offset = root_fret - form[root_string]
        position = 0
        if (max(form) + fret_offset) > MAX_FRETS:
            position = min(filter(lambda x:x >= 0, form)) + fret_offset

        # find the playing pattern at the nut
        line = ''
        for string,fret in enumerate(form):
            if fret == -1:  # string not played
                line += ' X '
            elif (fret+fret_offset) == 0:
                line += interval_ascii(intervals[string])
            else:
                if string == 0:
                    line += ' ▄▄' if position == 0 else ' ╟─'
                elif string == 5:
                    line += '▄▄ ' if position == 0 else '─┤ '
                else:
                    line += '▄▄▄' if position == 0 else ('─╫─' if string < 4 else '─┼─')
            if string < 5:
                line += '▄' if position == 0 else '─'

        out.append(line)
        if position == 0:
            out.append(' ╟───╫───╫───╫───┼───┤       ')

        ifret = position if position > 0 else 1
        while (ifret <= (max(form) + fret_offset)) or ((ifret - position) <= MAX_FRETS):
            line = ''
            for string,fret in enumerate(form):
                if (fret >= 0) and (ifret == (fret+fret_offset)):
                    line += interval_ascii(intervals[string])
                else:
                    line += ' ║ ' if string < 4 else ' │ '
                if string == 2:
                    if ifret in (3,5,7,9,15,17,19):
                        line += '●'
                    elif ifret == 12:
                        line += '○'
                    else:
                        line += ' '
                else:
                    line += ' '

            if (position != 0):
                if (ifret == position):
                    line += ' ' + position_ascii(position) + '  '
                else:
                    line += '       '

            out.append(line)
            out.append(' ╟───╫───╫───╫───┼───┤  ')
            ifret += 1

        return out


    def print_chord(self,root,type,chord_form=0):
        for line in self.diagram(root,type,chord_form):
            print(line)


    def list_sequences(self):
        print('\nChord Sequences:')
        print(" 0: Random")
        i = 1
        for sequence in self.chord_sequences:
            a = f'{i:2d}: {sequence[0]:20s} - '
            flag = False
            for chord in sequence[1:]:
                a += (', ' if flag else '') + chord
                if not flag:
                    flag = True
            print(a)
            i += 1


    def get_random_chord(self):
        return (
            self.notes[int(random.random()*len(self.notes))],
            self.formulas[int(random.random()*len(self.formulas))][0],
            int(random.random()*3)+1
        )

