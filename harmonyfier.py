import harmony
import constants
from random import choice, randrange

def getChord(chordType, rootDegree, degreesInKey) :
	if (chordType == 'triad') :
		return getTriad(rootDegree, degreesInKey)
	elif (chordType == 'sus2') :
		return getSus2(rootDegree, degreesInKey)
	elif (chordType == 'sus4') :
		return getSus4(rootDegree, degreesInKey)
	elif (chordType == '7th') :
		return get7th(rootDegree, degreesInKey)
	else :
		return getTriad(rootDegree, degreesInKey)

def getTriad(rootDegree, degreesInKey) :
	degrees = [rootDegree]
	third = rootDegree + 2
	if (third > degreesInKey) :
		third = third % degreesInKey
	fifth = third + 2
	if (fifth > degreesInKey) :
		fifth = fifth % degreesInKey
	degrees.extend([third, fifth])
	return degrees

def getSus2(rootDegree, degreesInKey) :
	degrees = [rootDegree]
	second = rootDegree + 1
	if (second > degreesInKey) :
		second = second % degreesInKey
	fifth = second + 3
	if (fifth > degreesInKey) :
		fifth = fifth % degreesInKey
	degrees.extend([second, fifth])
	return degrees

def getSus4(rootDegree, degreesInKey) :
	degrees = [rootDegree]
	fourth = rootDegree + 3
	if (fourth > degreesInKey) :
		fourth = fourth % degreesInKey
	fifth = fourth + 1
	if (fifth > degreesInKey) :
		fifth = fifth % degreesInKey
	degrees.extend([fourth, fifth])
	return degrees

def get7th(rootDegree, degreesInKey) :
	degrees = getTriad(rootDegree, degreesInKey)
	seventh = rootDegree + 6
	if (seventh > degreesInKey) :
		seventh = seventh % degreesInKey
	degrees.append(seventh)
	return degrees

def getDegreeLevel(degree) :
	if (degree in harmony._degreesByLevel['best']) :
		return 'best'
	elif (degree in harmony._degreesByLevel['good']) :
		return 'good'
	else :
		return 'bad'

def getNextChord(previousChord, key) :
	previousRootDegree = previousChord['root']
	previousDegreeLevel = getDegreeLevel(previousRootDegree)
	if (randrange(100) < harmony._repeatDegree[previousDegreeLevel]) :
		''' TODO susify '''
		return previousChord
	else :
		nbDegreesInKey = len(harmony._semitones[key])
		candidates = [1, 2, 3, 4, 5, 6]
		candidates.remove(previousRootDegree)
		if (key == 'minor' and previousRootDegree != 2) :
			candidates.remove(2)
		nextRootDegree = choice(candidates)
		chordType = choice(harmony._chordTypeAcceptance.keys())
		while (randrange(100) > harmony._chordTypeAcceptance[chordType]) :
			chordType = choice(harmony._chordTypeAcceptance.keys())
		if (chordType == 'triad') :
			if (nextRootDegree == 5 and randrange(100) < harmony._add7thToDomninant) :
				chordType = '7th';
			elif (randrange(100) < harmony._add7thToOthers) :
				chordType = '7th';
		degrees = getChord(chordType, nextRootDegree, nbDegreesInKey)
		duration = constants.WHOLE
		distance = nextRootDegree - previousRootDegree
		octave = previousChord['octave']
		if (abs(distance) > nbDegreesInKey / 2) :
			if (distance > 0) :
				octave = octave + 1
			else :
				octave = octave - 1
		return {'root': nextRootDegree, 'octave': octave, 'degrees': degrees, 'type': chordType, 'duration': duration}


next = {'root': 1, 'octave': 3, 'degrees': [1,3,5], 'type': 'triad', 'duration': constants.WHOLE}
print str(next)
for i in range(1,4) :
	next = getNextChord(next, 'minor')
	print str(next)

'''

	Augmenter proba sus2 et sus4 en cas de repetition d accords
	gerer cadences et transitions (cadences seulement et simplifier harmony.py, garder un random sur les degres acceptables au lieu des transitions)
	retournements
	7th sur autres que triad ?
	Duree d'accord par probabilite
		Si duree < mesure completer jusqu'a remplir la mesure (toujours un nouvel accord sur premier temps)


'''	