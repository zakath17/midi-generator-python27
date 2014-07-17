_semitones = {'major': {1:0, 2:2, 3:4, 4:5, 5:7, 6:9, 7:11},
	'minor': {1:0, 2:2, 3:4, 4:5, 5:7, 6:9, 7:11}}

_chordTypeAcceptance = {
	'triad': 100,
	'sus2': 5,
	'sus4': 5
}

_add7thToDomninant = 50

_add7thToOthers = 5

_endOnCadence = 80

_switch_sus_triad_on_repeat = 80

_degreesByLevel = {'best': [1, 4, 5],
	'good': [2, 6],
	'bad': [3]}

_repeatDegree = {'best': 20,
	'good': 5,
	'bad': 0}

_transitions = {'natural': [3, -3, 4, -4],
	'best': [-2, 5],
	'good': {4: [5], 5: [6], 6: [5]},
	'bad': {1: [2, 3], 2: [4], 3: [4], 5: [4], 6: [1]}}

_transitionsAcceptance = {'natural': 100,
	'best': 70,
	'good': 50,
	'bad': 10}

_cadences = {'best': [4, 5], 
	'good': [5],
	'bad': [4]}

_cadencesAcceptance = {'best': 70,
	'good': 50,
	'bad': 10}


def generateGrid(bars, key) :
	chordList = {'root': 0, 'degrees': [0, 2, 4], 'octave': 0}
	return {'chordList' : chordList, 'semitones': semitones[key]}


'''

TODO 
	harmonifier/cator -> ce fichier, et harmony contient des styles d'harmonies (7th, proba longueur des accords, cadences...)
	degre d acceptance des notes au lieu de keepOutOfChord : 1 - 7 (do mi sol si re fa la pour do majeur)
	5 ssi bar %2 = 0
	generer suite jusqu a bars - len(cadence) si une cadence est retenue
	cas particulier en mineur pour 2 a faire suivre par 5 pour etre acceptable
	enchainement 1 -> 2 entraine un retournement du 2
	une fois ok, refactoring du reste en enlevant key des parametres (le retour de la grid devrait suffire)

'''	