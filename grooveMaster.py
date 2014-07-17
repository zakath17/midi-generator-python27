from tools import *
from drums import *

def generateDrumPatterns(bars, style) :
	init = patternalize(bars, drumPatternsRepartition[style])
	patterns = []
	patterns = []
	for p in init :
		pLength = init[p][0]
		pLoops = init[p][1]
		patterns.append({'length': pLength, 'loops': pLoops})
	return patterns

def generateDrumBar(style, tck, currentBar, start, xCite, breakBar=False) :
	thisDrumParts = drumParts[style]
	stepFromResolution = RESOLUTION / 12
	bar = {}
	barHits = []
	steps = {}
	for i in range(1, MAX_STEP + 1) :
		steps[i] = {}
	barType = "std-"
	if (breakBar) :
		barType = "break-"
	for part in thisDrumParts :
		if (part in xCite) :
			add = xCite[part]
		else :
			add = 0
		for i in range(1, MAX_STEP+1, stepFromResolution) :
			if (i > MAX_STEP - 12) :
				thisBar = barType + "last"
			elif ((i // 12) % 2 == 0) :
				thisBar = barType + "even"
			else :
				thisBar = barType + "odd"
			stepBase12 = ((i / stepFromResolution) % 12)
			if (stepBase12 == 0) :
				stepBase12 = 12
			percentage = thisDrumParts[part][thisBar][stepBase12]
			if (percentage > 0) :
				percentage += add
			random = randrange(100)
			if (random + XCTBL < percentage) or (percentage == 100) :
				if (part == HHC) and (HHO in steps[i]) :
					break
				elif (part == HHO) and (HHC in steps[i]) :
					del steps[i][HHC]
				steps[i][part] = percentage
	notesOff = []
	for i in range(1, MAX_STEP + 1) :
		for pitch in notesOff :
			barHits.append(midi.NoteOffEvent(tick=tck, channel=9, data=[pitch, 0]))
			end = i
			tck = 0
		del notesOff[:]
		for pitch in steps[i].keys() :
			percentage = steps[i][pitch]
			if (percentage < DRUM_VELOCITY_THRESHOLD_LOW) :
				velocity = DRUM_VELOCITY_LOW
			elif (percentage < DRUM_VELOCITY_THRESHOLD_MED) :
				velocity = DRUM_VELOCITY_MED
			else :
				velocity = DRUM_VELOCITY_HIGH
			if (not barHits) :
				thisStart = start + ((i-1) * (currentBar + 1))
			barHits.append(midi.NoteOnEvent(tick=tck, channel=9, data=[pitch, velocity]))
			notesOff.append(pitch)
			tck = 0
		tck += 1
	for pitch in notesOff :
		barHits.append(midi.NoteOffEvent(tick=tck, channel=9, data=[pitch, 0]))
		end = i + 1
		tck = 0
	bar['hits'] = barHits
	bar['start'] = thisStart
	bar['end'] = end
	bar['tck'] = tck
	return bar

def generateDrumTrack(bars, loops, grid, style, xCite={}, insertBreak=True, volume=100) :
	drumPatterns = generateDrumPatterns(bars, style)
	trackHits = [midi.ControlChangeEvent(tick=0, channel=9, data=[7, volume])]
	loopHits = []
	currentPattern = 0
	for index, pattern in enumerate(drumPatterns) :
		currentPattern += 1
		patternHits = []
		pLength = pattern['length']
		pLoops = pattern['loops']
		currentBar = 0
		start = 0
		if (currentPattern > 1) and (drumPatterns[currentPattern-2]['loops'] < 2) :
			start = MAX_STEP + 1 - end
		end = 0
		tck = start
		while (currentBar < pLength) :
			if ((index == len(drumPatterns) - 1) and (currentBar == pLength - 1) and insertBreak) :
				breakHits = list(patternHits)
				startBreak = 0
				thisBar = generateDrumBar(style, tck, currentBar, start, xCite, True)
				if (pLength == 1) :
					startBreak = thisBar['start']
				endBreak = thisBar['end']
				breakHits.extend(thisBar['hits'])
			thisBar = generateDrumBar(style, tck, currentBar, start, xCite)
			if (not patternHits) :
				start = thisBar['start']
			end = thisBar['end']
			tck = thisBar['tck']
			patternHits.extend(thisBar['hits'])
			currentBar += 1
		i = 0
		delay = 0
		while (i < pLoops) :
			if ((index == len(drumPatterns) - 1) and (i == pLoops - 1) and insertBreak) :
				delay = MAX_STEP + 1 - end - startBreak
				firstHit = breakHits[0]
				hit = midi.NoteOnEvent(tick=firstHit.tick + delay, channel=9)
				hit.set_pitch(firstHit.get_pitch())
				hit.set_velocity(firstHit.get_velocity())
				breakHits[0] = hit
				loopHits.extend(breakHits)
			elif (i == 1) :
				delay = MAX_STEP + 1 - end - start
				firstHit = patternHits[0]
				hit = midi.NoteOnEvent(tick=firstHit.tick + delay, channel=9)
				hit.set_pitch(firstHit.get_pitch())
				hit.set_velocity(firstHit.get_velocity())
				patternHits[0] = hit
				loopHits.extend(patternHits)
			else :
				loopHits.extend(patternHits)
			i += 1
	i = 0
	while (i < loops) :
		if (i == 1) :
			if (insertBreak) :
				delay = MAX_STEP + 1 - endBreak
			else :
				delay = MAX_STEP + 1 - end
			firstHit = loopHits[0]
			hit = midi.NoteOnEvent(tick=firstHit.tick + delay, channel=9)
			hit.set_pitch(firstHit.get_pitch())
			hit.set_velocity(firstHit.get_velocity())
			loopHits[0] = hit
		trackHits.extend(loopHits)
		i += 1
	trackHits.append(midi.EndOfTrackEvent(tick=0, data=[]))
	return midi.Track(trackHits)