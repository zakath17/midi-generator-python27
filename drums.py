from constants import *

# QUARTER : 1
# EIGHTH : 1,7
# TRIPLET : 1,5,9
# SIXTEENTH : 1,4,7,10
# SEMITRIPLET : 1,3,5,7,9,11
# ZERO : 2,6,8,12

# Test
kick_test = {
	'std-even':{1:100, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'std-odd':{1:0, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'std-last':{1:0, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'break-even':{1:100, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'break-odd':{1:0, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'break-last':{1:0, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:XCTBL, 11:0, 12:0}}
snare_test = {
	'std-even':{1:0, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:2, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'std-odd':{1:100, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:2, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'std-last':{1:100, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:2, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'break-even':{1:0, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:2, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'break-odd':{1:100, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:2, 8:0, 9:0, 10:XCTBL, 11:0, 12:0},
	'break-last':{1:100, 2:0, 3:0, 4:XCTBL, 5:0, 6:0, 7:100, 8:0, 9:0, 10:100, 11:0, 12:0}}
hhc_test = {
	'std-even':{1:100, 2:0, 3:XCTBL, 4:XCTBL, 5:XCTBL, 6:0, 7:100, 8:0, 9:XCTBL, 10:XCTBL, 11:XCTBL, 12:0},
	'std-odd':{1:100, 2:0, 3:XCTBL, 4:XCTBL, 5:XCTBL, 6:0, 7:100, 8:0, 9:XCTBL, 10:XCTBL, 11:XCTBL, 12:0},
	'std-last':{1:100, 2:0, 3:XCTBL, 4:XCTBL, 5:XCTBL, 6:0, 7:100, 8:0, 9:XCTBL, 10:XCTBL, 11:XCTBL, 12:0},
	'break-even':{1:100, 2:0, 3:XCTBL, 4:XCTBL, 5:XCTBL, 6:0, 7:100, 8:0, 9:XCTBL, 10:XCTBL, 11:XCTBL, 12:0},
	'break-odd':{1:100, 2:0, 3:XCTBL, 4:XCTBL, 5:XCTBL, 6:0, 7:100, 8:0, 9:XCTBL, 10:XCTBL, 11:XCTBL, 12:0},
	'break-last':{1:100, 2:0, 3:XCTBL, 4:XCTBL, 5:XCTBL, 6:0, 7:100, 8:0, 9:XCTBL, 10:XCTBL, 11:XCTBL, 12:0}}
hho_test = {
	'std-even':{1:20, 2:0, 3:0, 4:0, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:0, 11:0, 12:0},
	'std-odd':{1:20, 2:0, 3:0, 4:0, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:0, 11:0, 12:0},
	'std-last':{1:20, 2:0, 3:0, 4:0, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:0, 11:0, 12:0},
	'break-even':{1:20, 2:0, 3:0, 4:0, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:0, 11:0, 12:0},
	'break-odd':{1:20, 2:0, 3:0, 4:0, 5:0, 6:0, 7:XCTBL, 8:0, 9:0, 10:0, 11:0, 12:0},
	'break-last':{1:20, 2:0, 3:0, 4:0, 5:0, 6:0, 7:10, 8:0, 9:0, 10:0, 11:0, 12:0}}

drumParts = {'test': {KICK: kick_test, SNARE: snare_test, HHC: hhc_test, HHO: hho_test}}

drumPatternsRepartition = {'test': {1:75, 2:75, 4:10, 8:5}}