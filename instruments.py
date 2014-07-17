from constants import *
from tools import *
from random import choice

genericBass = {
	'patternsRepartition': {1:75, 2:75, 4:10, 8:5},
	'rythm': rythm_solo,
	'gm': choice(range(32,40)),
	'restFactor': 10,
	'keepOutOfChord': 0,
	'distanceMaxBetweenNotes': 7,
	'firstInBarFirstInChord': 80,
	'backToChord': ZERO,
	'velocityRange': [100,100],
	'octaveLow': 0,
	'octaveHigh': 0,
	'chordFactor': chordFactor_none,
	'arpeggioMode': choice(arpeggiosOptions),
	'chordNotes': choice(chordNotesOptions)
}

lead = {
	'patternsRepartition': {1:20, 2:40, 4:75, 8:100},
	'rythm': rythm_solo,
	'gm': 26,
	'restFactor': 15,
	'keepOutOfChord': 30,
	'distanceMaxBetweenNotes': 7,
	'firstInBarFirstInChord': 50,
	'backToChord': ZERO,
	'velocityRange': [70,100],
	'octaveLow': 0,
	'octaveHigh': 1,
	'chordFactor': chordFactor_none,
	'arpeggioMode': "none",
	'chordNotes': chordNotes_all
}

pad = {
	'patternsRepartition': {1:5, 2:5, 4:75, 8:100},
	'rythm': rythm_paddy,
	'gm': 89,
	'restFactor': 2,
	'keepOutOfChord': 0,
	'distanceMaxBetweenNotes': 12,
	'firstInBarFirstInChord': 100,
	'backToChord': ZERO,
	'velocityRange': [100,100],
	'octaveLow': 0,
	'octaveHigh': 1,
	'chordFactor': chordFactor_all,
	'arpeggioMode': "none",
	'chordNotes': chordNotes_all
}

test = {
	'patternsRepartition': {1:100, 2:0.5, 4:0.5, 8:0},
	'rythm': rythm_only_eighth,
	'gm': 26,
	'restFactor': 0,
	'keepOutOfChord': 0,
	'distanceMaxBetweenNotes': 7,
	'firstInBarFirstInChord': 100,
	'backToChord': HALF,
	'velocityRange': [60,100],
	'octaveLow': 0,
	'octaveHigh': 0,
	'chordFactor': chordFactor_none,
	'arpeggioMode': "up",
	'chordNotes': chordNotes_all
}

instruments.update({
	'genericBass': genericBass,
	'lead': lead,
	'pad': pad,
	'test': test
})