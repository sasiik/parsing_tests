N = 7
PITCHES = ["до", "ре", "ми", "фа", "соль", "ля", "си"]
LONG_PITCHES = ["до-о", "ре-э", "ми-и", "фа-а", "со-оль", "ля-а", "си-и"]
INTERVALS = ["прима", "секунда", "терция", "кварта", "квинта", "секста", "септима"]


class Note:
    longNotes = {
        'до': 'до-о',
        "ре": "ре-э",
        "ми": "ми-и",
        "фа": "фа-а",
        "соль": "со-оль",
        "ля": "ля-а",
        'си': "си-и"
    }

    def __init__(self, note, is_long=False):
        self.note = note
        self.long = is_long
        self.keyIndex = list(Note.longNotes.keys()).index(self.note)

    def __eq__(self, other):
        if self.keyIndex == other.keyIndex:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.keyIndex == other.keyIndex:
            return False
        else:
            return True

    def __lt__(self, other):
        if self.keyIndex < other.keyIndex:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.keyIndex > other.keyIndex:
            return True
        else:
            return False

    def __le__(self, other):
        if self.keyIndex <= other.keyIndex:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.keyIndex >= other.keyIndex:
            return True
        else:
            return False

    def __rshift__(self, other):
        return self.__class__(list(Note.longNotes.keys())[(self.keyIndex + other) % 7], is_long=self.long)

    def __lshift__(self, other):
        res = self.keyIndex - other
        if res < 0:
            res = res % 7
        return self.__class__(list(Note.longNotes.keys())[res], is_long=self.long)

    def get_interval(self, other_note):
        global INTERVALS
        res = abs(self.keyIndex - other_note.keyIndex)
        return INTERVALS[res]

    def play(self):
        if self.long:
            return Note.longNotes[self.note]
        else:
            return self.note

    def __str__(self):
        return self.play()


class LoudNote(Note):
    def __init__(self, note, is_long=False):
        super().__init__(note, is_long)
        self.note = note.upper()

    def play(self):
        if self.long:
            return Note.longNotes[self.note.lower()].upper()
        else:
            return self.note


class NoteWithOctave(Note):
    def __init__(self, note, octave, is_long=False):
        super().__init__(note, is_long)
        self.octave = octave

    def play(self):
        if self.long:
            return Note.longNotes[self.note] + f' ({self.octave})'
        else:
            return self.note + f' ({self.octave})'


class DefaultNote(Note):
    def __init__(self, note='до', is_long=False):
        super().__init__(note, is_long)


class Melody:
    melody_note_copy = None

    def __init__(self, notes=None):
        if notes is None:
            notes = []
        if notes:
            self.notes = notes
            Melody.melody_note_copy = self.notes[:]
        else:
            self.notes = []

    def __str__(self):
        return ', '.join([elem.play() for elem in self.notes]).capitalize()

    def replace_last(self, note):
        self.notes = self.notes[:-1]
        self.notes.append(note)

    def remove_last(self):
        self.notes = self.notes[:-1]

    def append(self, note):
        self.notes.append(note)

    def clear(self):
        self.notes = []

    def __rshift__(self, other):
        global PITCHES
        copy = self
        res = []
        if all(0 <= elem.keyIndex < 7 - other for elem in copy.notes):
            for elem in copy.notes:
                elem.keyIndex += other
                elem.note = PITCHES[elem.keyIndex]
                res.append(Note(elem.note, elem.long))
            print([elem.play() for elem in res])
            return Melody(res)
        else:
            print([elem.play() for elem in res])
            return self

    def __lshift__(self, other):
        global PITCHES
        notes = self.notes[:]
        res = []
        if all(0 + other <= elem.keyIndex < 7 for elem in notes):
            for elem in notes:
                elem.keyIndex -= other
                elem.note = PITCHES[elem.keyIndex]
                res.append(Note(elem.note, elem.long))
            return Melody(res)
        else:
            return Melody(Melody.melody_note_copy)

    def __len__(self):
        return len(self.notes)


mel1 = Melody([Note('ре', True), Note('ми'), Note('до', True), Note('фа'), Note('ля'), Note('соль', True)])
m1 = mel1 >> 1
m2 = mel1 >> 3
print(m1)
print(m2)
print()
