from tools import *
from instruments import *

def generateRythmPatterns(bars, instrument) :
	init = patternalize(bars, instrument['patternsRepartition'])
	patterns = []
	for p in init :
		pLength = init[p][0]
		pLoops = init[p][1]
		patterns.append({'length': pLength, 
			'loops': pLoops,
			'rythm': generateRythmForPattern(pLength, instrument)})
	return patterns

def generateRythmForPattern(bars, instrument) :
	patternMaxStep = MAX_STEP * bars
	currentStep = 1
	steps = [0] * patternMaxStep
	while (currentStep <= patternMaxStep) :
		thisStep = generateRythmForStep(patternMaxStep, currentStep, instrument)
		steps[currentStep-1] = thisStep
		currentStep += thisStep
	return steps
	
def generateRythmForStep(patternMaxStep, currentStep, instrument) :
	rythm = instrument['rythm']
	while (True) :
		tmpStep = choice(rythm.keys())
		if (tmpStep > MAX_STEP) :
			continue
		probaStep = rythm[tmpStep]
		if (randrange(100) < probaStep) :
			while (currentStep + tmpStep > patternMaxStep + 1) :
				if (tmpStep == HALF_) :
					tmpStep = HALF
				elif (tmpStep == QUARTER_) :
					tmpStep = QUARTER
				elif (tmpStep == EIGHTH_) :
					tmpStep = EIGHTH
				else :
					tmpStep = tmpStep / 2
			if ((currentStep > (MAX_STEP + 1 - tmpStep)) and (randrange(100) > ACCEPT_OVERFLOW)) :
				continue
			elif (tmpStep == WHOLE) :
				if (currentStep % QUARTER != 1) :
					continue
			elif (tmpStep == HALF) :
				if (currentStep % QUARTER != 1) :
					continue
			elif (tmpStep == QUARTER) :
				if (currentStep % EIGHTH != 1) :
					continue
			elif (tmpStep == EIGHTH) :
				if (currentStep % SIXTEENTH != 1) or (currentStep == MAX_STEP - SIXTEENTH):
					continue
			elif (currentStep % tmpStep != 1) :
				continue
			return tmpStep
	

def getChordNotes(semitones, basePitch, previousOctave, previousDegree, chord, instrument) :
	chordDegree = chord[0]
	subChord = []
	for noteInChord in instrument['chordNotes'] :
		if (noteInChord < len(chord)) :
			subChord.append(chord[noteInChord])
	thisOctaveLow = instrument['octaveLow']
	thisOctaveHigh = instrument['octaveHigh']
	baseOctave = previousOctave
	minPitch = basePitch + semitones[1] + (12 * thisOctaveLow)
	maxPitch = basePitch + semitones[1] + 11 + (12 * thisOctaveHigh)
	previousPitch = basePitch + semitones[previousDegree] + (12 * previousOctave)
	rootPitch = basePitch + semitones[chordDegree] + (12 * baseOctave)
	distance = rootPitch - previousPitch
	if ((distance > 0) and (distance < 12/2) and (thisOctaveHigh > baseOctave)) :
		baseOctave += 1
	if (rootPitch - previousPitch > maxPitch) and (thisOctaveLow < baseOctave) :
		baseOctave -= 1
	while True :
		rootPitch = basePitch + semitones[chordDegree] + (12 * baseOctave)
		lastPitch = basePitch + semitones[subChord[len(subChord) - 1]] + (12 * baseOctave)
		if (lastPitch < rootPitch) :
			lastPitch += 12
		if (lastPitch > maxPitch) and (thisOctaveLow < baseOctave) :
			baseOctave -= 1
		else :
			break
	notes = []
	for degree in subChord :
		noteOctave = baseOctave
		notePitch = basePitch + semitones[degree] + (12 * noteOctave)
		if (notePitch < rootPitch) and (thisOctaveHigh > noteOctave) :
			notePitch += 12
			noteOctave += 1
		notes.append({'degree':degree, 'pitch':notePitch, 'octave':noteOctave})
		if (degree == chordDegree) :
			root = {'degree': degree, 'pitch':notePitch, 'octave':noteOctave}
	return {'notes': notes, 'root': root}

def getNoteRange(basePitch, semitones, previousDegree, previousOctave, instrument, chord=None, ignoreDistance=False) :
	minPitch = basePitch + semitones[1] + (12 * instrument['octaveLow'])
	maxPitch = basePitch + semitones[1] + 11 + (12 * instrument['octaveHigh'])
	if (not ignoreDistance) :
		actualMinPitch = basePitch + semitones[previousDegree] + (previousOctave * 12) - instrument['distanceMaxBetweenNotes']
		actualMaxPitch = basePitch + semitones[previousDegree] + (previousOctave * 12) + instrument['distanceMaxBetweenNotes']
		if (actualMinPitch > minPitch) :
			minPitch = actualMinPitch
		if (actualMaxPitch < maxPitch) :
			maxPitch = actualMaxPitch
	subChord = []
	if (not chord is None) :
		for noteInChord in instrument['chordNotes'] :
			if (noteInChord < len(chord)) :
				subChord.append(chord[noteInChord])
	pitch = basePitch + semitones[previousDegree] + 12 * previousOctave
	degree = previousDegree
	octave = previousOctave
	noteRange = []
	while (pitch >= minPitch) :
		if ((chord is None) or (degree in subChord)) :
			noteRange.append({'degree':degree, 'pitch':pitch, 'octave':octave})
		degree -= 1
		if (degree == 0) :
			degree = len(semitones)
			octave -=1
		pitch = basePitch + semitones[degree] + 12 * octave
	degree = previousDegree + 1
	octave = previousOctave
	if (degree > len(semitones)) :
			degree = 1
			octave +=1
	pitch = basePitch + semitones[degree] + 12 * octave
	while (pitch <= maxPitch) :
		if ((chord is None) or (degree in subChord)) :
			noteRange.append({'degree':degree, 'pitch':pitch, 'octave':octave})
		degree += 1
		if (degree > len(semitones)) :
			degree = 1
			octave +=1
		pitch = basePitch + semitones[degree] + 12 * octave
	return noteRange

def getNextNoteInArpeggio(arpeggioRange, arpeggioMode, previousPitch, instrument, isFirst) :
	if (arpeggioMode == 'random') :
		return choice(arpeggioRange)
	else :
		if ('currentArpeggioMode' in instrument) :
			currentArpeggioMode = instrument['currentArpeggioMode']
		else :
			currentArpeggioMode = arpeggioMode
		arpeggioRange = quickSort(arpeggioRange)
		previousIndex = 0
		for note in arpeggioRange :
			if (note['pitch'] == previousPitch) :
				break
			previousIndex += 1
		if (isFirst) :
			instrument['currentArpeggioMode'] = arpeggioMode
			if (arpeggioMode == 'up') or (arpeggioMode == 'updown') :
				nextIndex = 0
			else :
				nextIndex = len(arpeggioRange) - 1
		elif (currentArpeggioMode == 'up') or (currentArpeggioMode == 'updown') :
			if (previousIndex + 1 == len(arpeggioRange)) :
				if (currentArpeggioMode == 'up') :
					nextIndex = 0
				else :
					nextIndex = len(arpeggioRange) - 2
					instrument['currentArpeggioMode'] = 'down'
			else :
				nextIndex = previousIndex + 1
		else :
			if (previousIndex - 1 < 0) :
				if (currentArpeggioMode == 'down') :
					nextIndex = len(arpeggioRange) - 1
				else :
					nextIndex = 1
					instrument['currentArpeggioMode'] = 'up'
			else :
				nextIndex = previousIndex - 1
		return arpeggioRange[nextIndex]


def getRandomNote(semitones, isFirst, noteLength, chord, nextChord, 
		basePitch, previousDegree, previousOctave, overflow, instrument) :
	arpeggioMode = instrument['arpeggioMode']
	if (arpeggioMode != 'none') :
		arpeggioRange = getNoteRange(basePitch, semitones, previousDegree, previousOctave, instrument, chord, True)
		previousPitch = basePitch + semitones[previousDegree] + 12 * previousOctave
		return getNextNoteInArpeggio(arpeggioRange, arpeggioMode, previousPitch, instrument, isFirst) 
	elif (isFirst) :
		if (randrange(100) <= instrument['firstInBarFirstInChord']) :
			chordNotes = getChordNotes(semitones, basePitch, previousOctave, previousDegree, chord, instrument)
			return chordNotes['root']
		else :
			return choice(getNoteRange(basePitch, semitones, previousDegree, previousOctave, instrument, chord))
	elif (noteLength > QUARTER) or (instrument['keepOutOfChord'] == 0) :
		if (overflow) :
			return choice(getNoteRange(basePitch, semitones, previousDegree, previousOctave, instrument, nextChord))
		else :
			return choice(getNoteRange(basePitch, semitones, previousDegree, previousOctave, instrument, chord))
	else :
		noteRange = getNoteRange(basePitch, semitones, previousDegree, previousOctave, instrument)
		condition = True
		while (condition) :
			candidate = choice(noteRange)
			if ((candidate['degree'] in chord) or (randrange(100) <= instrument['keepOutOfChord'])) :
				if (overflow) :
					if (candidate['degree'] in nextChord) :
						condition = False
					elif (randrange(100) <= instrument['keepOutOfChord']) :
						condition = False
				else :
					condition = False
		return candidate

def generateInstrumentTrack(bars, loops, key, basePitch, grids, instrument, volume=100) :
	channel = getNextAvailableChannel()
	rythmPatterns = generateRythmPatterns(bars, instrument)
	currentTick = ZERO
	previousDegree = 1
	previousOctave = 0
	currentBar = 0
	currentStep = 0
	currentChord = grids[0]
	trackNotes = [midi.ProgramChangeEvent(tick=ZERO, channel=channel, data=[instrument['gm']]),
		midi.ControlChangeEvent(tick=0, channel=channel, data=[7, volume])]
	loopNotes = []
	for pattern in rythmPatterns :
		length = pattern['length']
		ploops = pattern['loops']	
		rythm = pattern['rythm']
		rest = 0
		i = 0
		while (i < ploops) :
			patternNotes = []
			isFirst = True
			for noteLength in rythm :
				currentStep += 1
				relativeStep = currentStep%MAX_STEP
				if (relativeStep == 0) :
					relativeStep = MAX_STEP
				if (noteLength > 0) :
					if (randrange(100) < instrument['restFactor']) :
						rest += noteLength
					else :
						chord = KEYS[key]['chords'][currentChord]
						nextChord = None
						overflow = False
						subLength1 = noteLength
						subLength2 = 0
						if (relativeStep + noteLength > (MAX_STEP + 1)) :
							overflow = True
							nextChord = KEYS[key]['chords'][grids[currentBar+1]]
							while (relativeStep + subLength1 > (MAX_STEP + 1)) :
								subLength1 = subLength1 - SEMITRIPLET
								subLength2 = noteLength - subLength1
						semitones = KEYS[key]['semitones']
						if (randrange(100) < instrument['chordFactor'][subLength1]) :
							isChord = True
							tmp = getChordNotes(semitones, basePitch, previousOctave, previousDegree, chord, instrument)
							notes = tmp['notes']
							if (overflow) :
								noteLength = subLength1
								rythm[relativeStep + (MAX_STEP * currentBar) - 1] = subLength1
								position = relativeStep + (MAX_STEP * currentBar) + subLength1 - 1
								if (len(rythm) > position) :
									rythm[relativeStep + (MAX_STEP * currentBar) + subLength1 - 1] = subLength2
						else :
							isChord = False
							notes = [getRandomNote(semitones, isFirst, noteLength, chord, nextChord, basePitch, 
								previousDegree, previousOctave, overflow, instrument)]
						for pos, note in enumerate(notes) :
							if (pos == 0) :
								previousDegree = note['degree']
								previousOctave = note['octave']
								velocityMin = instrument['velocityRange'][0]
								velocityMax = instrument['velocityRange'][1]
								thisVelocity = choice(range(velocityMin, velocityMax + VELOCITY_STEP, VELOCITY_STEP))
								noteEvent = midi.NoteOnEvent(tick=ZERO + rest, channel=channel)
							else :
								noteEvent = midi.NoteOnEvent(tick=ZERO, channel=channel)
							noteEvent.set_pitch(note['pitch'])
							velocityMin = instrument['velocityRange'][0]
							velocityMax = instrument['velocityRange'][1]
							noteEvent.set_velocity(thisVelocity)
							patternNotes.append(noteEvent)
						for pos, note in enumerate(notes) :
							if (pos == 0) :
								noteEvent = midi.NoteOffEvent(tick=noteLength, channel=channel)
							else :
								noteEvent = midi.NoteOffEvent(tick=ZERO, channel=channel)
							noteEvent.set_pitch(note['pitch'])
							noteEvent.set_velocity(0)
							patternNotes.append(noteEvent)
						rest = 0
						isFirst = False
				if (relativeStep == MAX_STEP) :
					currentBar += 1
					isFirst = True
					if (currentBar < len(grids)) :
						currentChord = grids[currentBar]
				elif (instrument['backToChord'] != ZERO) and (relativeStep%instrument['backToChord'] == 0) :
					isFirst = True
			loopNotes.extend(patternNotes)
			i += 1
		i = 0
	while (i < loops) :
		if ((rest > 0) and (i > 0)) :
			firstNote = loopNotes[0]
			note = midi.NoteOnEvent(tick=firstNote.tick + rest, channel=channel)
			note.set_pitch(firstNote.get_pitch())
			note.set_velocity(firstNote.get_velocity())
			loopNotes[0] = note
		trackNotes.extend(loopNotes)
		i += 1
	trackNotes.append(midi.EndOfTrackEvent(tick=ZERO, data=[]))
	return midi.Track(trackNotes)