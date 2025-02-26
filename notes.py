# this will be able to take a root note and give me the nth step from it (+/-)
import random
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

notes_lookup = {}
for i, n in enumerate(zip(NOTE_NAMES, NOTE_NAMES_FLAT)):
    if n[0] == n[1]:
        notes_lookup[n[0]] = i
    else:
        notes_lookup[n[0]] = i
        notes_lookup[n[1]] = i


CHORD_SHAPES = {
    "minor": [0, 3, 7],
    "major": [0, 4, 7],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
}

SCALES = {
    # Major & Diatonic Modes
    "ionian": [0, 2, 4, 5, 7, 9, 11],  # Major scale
    "dorian": [0, 2, 3, 5, 7, 9, 10],  # Minor with raised 6th
    "phrygian": [0, 1, 3, 5, 7, 8, 10],  # Minor with lowered 2nd
    "lydian": [0, 2, 4, 6, 7, 9, 11],  # Major with raised 4th
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],  # Major with lowered 7th
    "aeolian": [0, 2, 3, 5, 7, 8, 10],  # Natural minor
    "locrian": [0, 1, 3, 5, 6, 8, 10],  # Minor with lowered 2nd and 5th
    # Harmonic & Melodic Minor Variations
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],  # Natural minor with raised 7th
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],  # Natural minor with raised 6th & 7th
    "dorian_b2": [0, 1, 3, 5, 7, 9, 10],  # Dorian with lowered 2nd
    "lydian_augment": [0, 2, 4, 6, 8, 9, 11],  # Lydian with augmented 5th
    "lydian_dominant": [0, 2, 4, 6, 7, 9, 10],  # Lydian with lowered 7th
    "mixolydian_b6": [0, 2, 4, 5, 7, 8, 10],  # Mixolydian with lowered 6th
    "locrian_natural_6": [0, 1, 3, 5, 6, 9, 10],  # Locrian with natural 6th
    # Pentatonic & Blues Scales
    "major_pentatonic": [0, 2, 4, 7, 9],  # 5-note scale (major)
    "minor_pentatonic": [0, 3, 5, 7, 10],  # 5-note scale (minor)
    "blues": [0, 3, 5, 6, 7, 10],  # Minor pentatonic + blue note
    # Symmetric Scales
    "whole_tone": [0, 2, 4, 6, 8, 10],  # Every step is a whole step
    "diminished_whole_half": [0, 2, 3, 5, 6, 8, 9, 11],  # Diminished (Whole-Half)
    "diminished_half_whole": [0, 1, 3, 4, 6, 7, 9, 10],  # Diminished (Half-Whole)
    # Exotic & Non-Western Scales
    "phrygian_dominant": [0, 1, 4, 5, 7, 8, 10],  # Spanish/Jewish scale
    "double_harmonic_major": [0, 1, 4, 5, 7, 8, 11],  # Byzantine/Middle Eastern
    "enigmatic": [0, 1, 4, 6, 8, 10, 11],  # Strange chromatic scale
    "hungarian_minor": [0, 2, 3, 6, 7, 8, 11],  # Eastern European minor scale
    "neapolitan_major": [0, 1, 3, 5, 7, 9, 11],  # Neapolitan major
    "neapolitan_minor": [0, 1, 3, 5, 7, 8, 11],  # Neapolitan minor
}


def get_note(note_name: str, offset: int) -> str:
    """
    Gets a note with an optional offset in half steps
    :param note_name:
    :param offset:
    :return:
    """
    note = notes_lookup.get(note_name, None)
    if note is None:
        raise KeyError(f"No note named {note_name}")

    if offset:
        note = note + offset

    if "b" in note_name:  # If the root was a flat note, use the flat notation
        return NOTE_NAMES_FLAT[note % 12]
    else:
        return NOTE_NAMES[note % 12]


def get_note_pattern(root, pattern):
    notes = []
    for note in pattern:
        notes.append(get_note(root, note))
    return notes


def get_chord(root: str, chord_type: str) -> list[str]:
    """
    Builds a chord from a root note and a step pattern
    :param root: The root note
    :param chord_type:
    :return:
    """
    chord_pattern = CHORD_SHAPES.get(chord_type.lower(), None)

    if chord_pattern is None:
        raise KeyError("Unknown chord type")

    chord = get_note_pattern(root, chord_pattern)

    return chord


def invert_chord(chord: list[str], inversion: int) -> list[str]:
    if inversion not in [0, 1, 2]:
        raise ValueError("Invalid inversion")

    match inversion:
        case 0:
            return chord
        case _:
            return chord[inversion:] + chord[:inversion]


def get_scale(root: str, scale: str) -> list[str]:
    scale_pattern = SCALES.get(scale.lower(), None)

    if scale_pattern is None:
        raise KeyError("Unknown chord type")

    scale = get_note_pattern(root, scale_pattern)

    return scale







class Chord:

    def __init__(self, root: str, chord_type: str):
        self.root = root
        self.chord_type = chord_type
        self.notes = self.get_chord()

    def __repr__(self):
        return f"{self.root} {self.chord_type}: {self.notes}"

    @staticmethod
    def get_note_pattern(root, pattern):
        notes = []
        for note in pattern:
            notes.append(get_note(root, note))
        return notes

    def get_chord(self) -> list[str]:
        """
        Builds a chord from a root note and a step pattern
        :param root: The root note
        :param chord_type:
        :return:
        """
        chord_pattern = CHORD_SHAPES.get(self.chord_type.lower(), None)

        if chord_pattern is None:
            raise KeyError("Unknown chord type")

        chord = get_note_pattern(self.root, chord_pattern)

        return chord

    def invert_chord(chord: list[str], inversion: int) -> list[str]:
        if inversion not in [0, 1, 2]:
            raise ValueError("Invalid inversion")

        match inversion:
            case 0:
                return chord
            case _:
                return chord[inversion:] + chord[:inversion]



def draw_notes(n: int = 4):
    print(f"Drawing {n} notes")

    indicies = {}
    # picks 4 notes (not allowing already chosen notes)
    # picks a chord for each note (can be the same)
    while len(indicies) < n:
        note_index = random.randint(0,len(NOTE_NAMES)-1)
        if note_index in indicies:
            continue
        chord_index = random.randint(0, len(CHORD_SHAPES.keys())-1)
        chord_name = [*CHORD_SHAPES.keys()][chord_index]
        chord = Chord(NOTE_NAMES[note_index], chord_name)
        note = NOTE_NAMES[note_index]
        indicies[note] = chord

    return [chord for note,chord in indicies.items()]


print(get_note("C", 0))
print(get_note("C", 3))
print(get_note("G", 7))
print(get_chord("C", "minor"))
print(get_chord("Db", "minor"))
print(invert_chord(get_chord("C", "major"), 0))
print(invert_chord(get_chord("C", "major"), 1))
print(invert_chord(get_chord("C", "major"), 2))
print(get_scale("C", "ionian"))

print(draw_notes(4))