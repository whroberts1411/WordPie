#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:         constants.py
#
# Purpose:      Global constants and variables for the WordPie program.
#
# Author:       Bill Roberts
#
# Created:      07/03/2022
#
# Amended:
#
#-------------------------------------------------------------------------------

# Colours for the letter and button backgrounds
GREEN = "#c9fb96"
GOLD = "#deea07"
GREY = "#C6D8D8"
WHITE = '#ffffff'
BLUE = '#0000e1'        # this is the text colour for the guesses
BTNCOLOUR = "#fffaf0"   # this is the default pale yellow colour
BTNDISABLED = '#c9c9c9' # The light grey used for the main window background

# This is the word we need to find
secret = ''
# Storage for possible letters at each word position (as sets)
letterSets = []
# Set of correct letters in the wrong position
wrongPos = set()
# Print messages to the terminal for matches and other debug info?
debug = False
# Current word and letter in the guesses grid
curr_word = None
curr_letter = None
# Store textbox controls for the grid - 6 sublists, one per row
wordGrid = []
# Store the textbox variables for the grid - 6 sublists, one per row
varsGrid = []
# Dictionary to store the keyboard button controls - key is the letter
keyboard = {}

#-------------------------------------------------------------------------------

# Storage for our word list, used in the wordpie.py module only.
wordDict = {}
candidates = []

#-------------------------------------------------------------------------------
