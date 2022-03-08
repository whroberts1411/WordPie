#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         wordpie.py
#
# Purpose:      Implements the Wordle word game, offering the option of either
#               trying to solve it yourself or letting the program attempt it.
#               It uses a dictionary of 2,500+ 5-letter words as its source.
#
# Author:       Bill Roberts
#
# Created:      19/01/2022
#
# Amended:      02/02/2022
#               Add an additionalcheck for auto completion, so that each new
#               word selected contains the letters that were not in the
#               correct position, as well as those that were.
#               14/02/2022
#               Start an amended version of the original program, that more
#               closely follows the online version, including an on-screen
#               keyboard.The program also has the option of adding words to the
#               dictionary while the game is being played, as the word list
#               used is missing quite a few common words and plurals.
#               01/03/2022
#               When selecting the "best word" to start a non-manual game, only
#               pick words with no duplicated letters, to maximise the chance
#               of finding the secret word.
#
#-------------------------------------------------------------------------------

import constants as c
import random

#-------------------------------------------------------------------------------

def setupDataframe():
    """ Read the wordlist file into a dictionary, and add the word score as the
        dictionary value. The score will be calculated from a file of letter
        frequencies in English words.   """

    # Store the wordlist file in a dictionary, with all values set to zero
    c.wordDict = {}
    with open('wordlist.csv', 'r') as myWords:
        for word in myWords:
            c.wordDict[word.replace('\n','')] = 0

    # Create a dictionary of letters and their frequencies
    frequency = {}
    with open('frequency.csv', 'r') as frequencies:
        for freq in frequencies:
            (key, val) = freq.split(',')
            frequency[key] = float(val)

    # Update wordDict with the calculated score for each word
    for word in c.wordDict:
        score = 0
        for letter in word:
            score += frequency[letter.upper()]
        c.wordDict[word] = score

#-------------------------------------------------------------------------------

def wordFound(word):
    """ Check if the supplied word is in the dictionary """

    if word in c.wordDict:
        return True
    else:
        return False

#-------------------------------------------------------------------------------

def getSecretWord(debug=False):
    """ Get a random word from the dictionary """

    secret, score = random.choice(list(c.wordDict.items()))

    if debug:
        print('-'*40)
        print('The secret word is ' + secret.upper())

    return secret

#-------------------------------------------------------------------------------

def getBestWord(debug=False):
    """ Get a random high-score word from the dictionary. Select all rows where
        the score is more than 0.375, then take a random row from this
        selection that doesn't have any duplicate letters. Using the base word
        list, this gives a possible selection of 136 words to choose from.  """

    # Store the candidate words in a list, for auto completion of the puzzle
    dictKeys = c.wordDict.keys()
    c.candidates =list(dictKeys)

    while True:
        word, score = random.choice(list(c.wordDict.items()))
        if score > 0.375 and len(set(word)) == 5:
            break

    if debug:
        print('\nCandidate words :', len(c.candidates))
        if len(c.candidates) < 30: print(c.candidates)
        print('New word selected :', word)

    return word

#-------------------------------------------------------------------------------

def getNextWord(letterSets, wrongPos, debug=False):
    """ Modify the candidate word list,depending on the previous result.
        Then, return a new guess word from this modified list.
        'letterSets' - possible letter options for each position in the word
        'wrongPos' - letters present but in wrong position       """

    # Only keep words from the candidates list that match the letters
    # stored in letterSets, for each letter position.
    c.candidates = [wrd for wrd in c.candidates
                                if matchWord(wrd, letterSets, wrongPos)]

    # Just in case something goes horribly wrong....
    if len(c.candidates) == 0: return 'ERROR'

    # Select a random word from the amended candidates list.
    word = random.choice(c.candidates)

    if debug:
        print('\n',wrongPos)
        print('Candidate words :', len(c.candidates))
        if len(c.candidates) < 60: print(c.candidates)
        print('New word selected :', word)

    return word

#-------------------------------------------------------------------------------

def matchWord(word, letterSets, wrongPos):
    """ Check if each letter in the word is present in the corresponding
        set of letters held in letterSets. Return True if found, else False. """

    for idx in range(5):
        if word[idx] not in letterSets[idx]:
            return False

    # Are all the gold (yellow) letters present in the word?
    if wrongPos.issubset(set(word)): return True
    else: return False

#-------------------------------------------------------------------------------

def getHint():
    """ Return a random word from the word list as a hint for the player.  """

    hint, score =  random.choice(list(c.wordDict.items()))
    return hint

#-------------------------------------------------------------------------------

def addNewWord(word):
    """ Add a new word to the csv word file and reload the dataframe. """

    with open('wordlist.csv', 'a', encoding='utf-8') as file:
        file.write('\n' + word)
    c.wordDict[word] = 0

#-------------------------------------------------------------------------------

def main():
    """ Start point for this module, when run in isolation for testing.  """

    setupDataframe()
    temp = getSecretWord()
    print('Secret Word :', temp)

    return

    # Do a disassembly of a function to see what python is doing.
    import dis
    print('-'*50)
    dis.dis(matchWord)
    print('-'*50)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

#-------------------------------------------------------------------------------
