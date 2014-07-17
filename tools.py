from keys import *
from random import choice, randrange


rythm_paddy = {WHOLE:100, HALF_:70, HALF:90, QUARTER_:0, QUARTER:0, EIGHTH_:0, EIGHTH:0, TRIPLET:0, SIXTEENTH:0, SEMITRIPLET:0}
rythm_solo = {WHOLE:2, HALF_:5, HALF:15, QUARTER_:40, QUARTER:70, EIGHTH_:20, EIGHTH:75, TRIPLET:10, SIXTEENTH:10, SEMITRIPLET:5}
rythm_only_eighth = {WHOLE:0, HALF_:0, HALF:0, QUARTER_:0, QUARTER:0, EIGHTH_:0, EIGHTH:100, TRIPLET:0, SIXTEENTH:0, SEMITRIPLET:0}

chordFactor_none = {WHOLE:0, HALF_:0, HALF:0, QUARTER_:0,  QUARTER:0, EIGHTH_:0, EIGHTH:0, TRIPLET:0, SIXTEENTH:0, SEMITRIPLET:0}
chordFactor_all = {WHOLE:100, HALF_:100, HALF:100, QUARTER_:100, QUARTER:100, EIGHTH_:100, EIGHTH:100, TRIPLET:100, SIXTEENTH:100, SEMITRIPLET:100}

arpeggiosOptions = ["up", "down", "updown", "downup", "random", "none"]
chordNotes_all = [0,1,2,3,4,5]
chordNotes_power = [0,2]
chordNotes_root = [0]
chordNotesOptions = [chordNotes_root, chordNotes_power, chordNotes_all]

nextChannel = 0
instruments = {}

def patternalize(bars, repartition) :
	patterns = {}
	current = 0
	done = 0
	while (bars > 0) :
		thisLength = 0
		if ((bars % 2) != 0) :
			thisLength = 1
		else :
			range = [1]
			if ((bars % 4) != 0) :
				range.append(2)
			elif ((bars % 8) != 0) :
				range.extend([4,2])
			else :
				range.extend([8,4,2])
			while (thisLength == 0) :
				tmpLength = choice(range)
				if (randrange(100) < repartition[tmpLength]) :
					thisLength = tmpLength
		if ((current == 0)or(patterns[current-1][0] != thisLength)) :
			patterns[current] = [thisLength, 1]
			current += 1
		else  :
			if ((done%8 == 0) and (thisLength != 8)) :
				patterns[current] = [thisLength, 1]
				current += 1
			else :
				patterns[current-1][1] += 1
		bars -= thisLength
		done += thisLength
	return patterns

def generateGridPatterns(bars, chosenKey, complexity) :
	key = KEYS[chosenKey]
	init = patternalize(bars, gridPatternsRepartition)
	grid = []
	for p in init :
		pLength = init[p][0]
		pLoops = init[p][1]
		probability = 0
		while (probability <= randrange(100)) :
			pGrid = choice(key['grids'][str(pLength) + complexity])
			probability = pGrid[0]
		i = 0
		while (i < pLoops) :
			grid.extend(pGrid[1])
			i += 1
	return {'patterns': init, 'grid': grid}

def getNextAvailableChannel() :
	global nextChannel
	toReturn = nextChannel
	if (nextChannel == 15) :
		raise NameError('Too many tracks, maximum is 15 plus drums')
	elif (nextChannel == 8) :
		nextChannel += 2
	else :
		nextChannel += 1
	return toReturn


def quickSort(lst):
    if lst == []: 
        return []
    else:
        pivot = lst[0]
        lesser = quickSort([x for x in lst[1:] if x['pitch'] < pivot['pitch']])
        greater = quickSort([x for x in lst[1:] if x['pitch'] >= pivot['pitch']])
        return lesser + [pivot] + greater