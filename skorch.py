import midi
from constants import *
from tools import *
from grooveMaster import *
from instruments import *
from melodyMaker import *

bars = 4
loops = 2
tempo = 110
chosenKey = 'major'
rootNote = midi.C_4
complexity = 'basic'
name = "midiFile"

# Master Track
master = [midi.SetTempoEvent(bpm=tempo),
	midi.TimeSignatureEvent(tick=0, data=[TIME_SIGNATURE_NUM, TIME_SIGNATURE_DEN/2, 24, 8]),
	midi.EndOfTrackEvent(tick=0, data=[])]
tracks = [midi.Track(master)]

# Grid
gridRythm = generateGridPatterns(bars, chosenKey, complexity)
gridLead = gridRythm['grid']
i = 1
while (i < loops) :
	gridLead.extend(gridRythm['grid'])
	i += 1

# Drums
xCite = {HHC:10, KICK:5, SNARE:5}
tracks.append(generateDrumTrack(bars, loops, gridRythm['patterns'], 'test', xCite=xCite, insertBreak=True))

# Instruments
#tracks.append(generateInstrumentTrack(bars, loops, chosenKey, rootNote - 12, gridRythm['grid'], instrument=instruments['genericBass']))
tracks.append(generateInstrumentTrack(bars, loops, chosenKey, rootNote, gridRythm['grid'], instrument=instruments['pad'], volume=80))
tracks.append(generateInstrumentTrack(bars * loops, 1, chosenKey, rootNote, gridLead, instrument=instruments['test'], volume=80))

# Write to file
midiFile = midi.Pattern(tracks=tracks, resolution=RESOLUTION)
midi.write_midifile("output/" + name + ".mid", midiFile)

''' 

Todo

	- Rework harmony pour rapprocher les accords grace aux inversions (générer aleatoirement au lieu de listes statiques ?)
	- Pattern loop > 1 -> transposer les notes en fonction des accords au lieu d en regenerer
	- Mettre en place des phrases musicales (rest en fin de phrase de longueur +- parametre dependant de l instrument)
	- Etoffer les instruments et drums (shitty rythm pour genericBass)
	- Mettre en place des demies mesures pour les patterns (ou juste les grids ?)
	- Séparer les instruments en plusieurs fichiers par categorie (bass, pad, lead) 
	- Creer des gabarits de beat dans ultimateRandomizer
	- Faire des scenes regroupables en song
	- Voir si le morceau et les pistes peuvent avoir un nom
	- UI : Drums, Percussions et 8 pistes instruments (+ gestion sections)

'''