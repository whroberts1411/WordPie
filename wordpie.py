#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:         wordle.py
#
# Purpose:      Implements the Wordle word game, offering the option of either
#               trying to solve it yourself or letting the program attempt it.
#               It uses a dictionary of 2,498 5-letter words as its source.
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

import pandas as pd
import random

wordDict = None
candidates = []

#-------------------------------------------------------------------------------

def setupDataframe():
    """ Modify the dataframe to name the word column and add a second column
        for the word scores. These will be derived from a file of letter
        frquencies held in 'frequency.csv'.   """

    global wordDict

    wordDict = pd.read_csv('wordlist.csv', header=None)

    # Rename the first column that holds the 5-letter words
    wordDict.rename(columns={0:'word'}, inplace=True)

    # Create a list of all zeros, same length as the dataframe
    zerolist = [0 for i in range(len(wordDict.index))]

    # Create a new column initialised to all zeros
    wordDict['score'] = zerolist

    # Create a dictionary of letters and their frequencies
    frequency = pd.read_csv('frequency.csv', header=0, index_col=0,
                            squeeze=True).to_dict()

    # Update the 'score' column with the calculated score for each word
    for idx in range(len(wordDict.index)):
        word = wordDict.iloc[idx][0]
        score = 0
        for letter in word:
            score += frequency[letter.upper()]
        wordDict.loc[idx, 'score'] = score

#-------------------------------------------------------------------------------

def wordFound(word):
    """ Check if the supplied word is in the dictionary """

    if word in wordDict.values:
        return True
    else:
        return False

#-------------------------------------------------------------------------------

def getSecretWord(debug=False):
    """ Get a random word from the dictionary """

    secret = wordDict.sample().values[0][0]

    if debug:
        print('-'*40)
        print('The secret word is ' + secret.upper())

    return secret

#-------------------------------------------------------------------------------

def getBestWord(debug=False):
    """ Get a random high-score word from the dictionary. Select all rows where
        the score is more than 0.4, then take a random row from this selection.
        Finally, get the value of the first cell and return it. """

    # Store the candidate words in a list, for auto completion of the puzzle
    global candidates
    candidates = wordDict['word'].tolist()

    while True:
        word = wordDict[wordDict.score > 0.4].sample().values[0][0]
        if len(set(word)) == 5: break

    if debug:
        print('\nCandidate words :', len(candidates))
        if len(candidates) < 30: print(candidates)
        print('New word selected :', word)

    return word

#-------------------------------------------------------------------------------

def getNextWord(letterSets, wrongPos, debug=False):
    """ Modify the candidate word list,depending on the previous result.
        Then, return a new guess word from this modified list.
        'letterSets' - possible letter options for each position in the word
        'wrongPos' - letters present but in wrong position
    """

    global candidates
    # Remove all words from the candidates list that don't match the letters
    # stored in letterSets, for each letter position.
    candidates = [word for word in candidates if matchWord(word, letterSets)]

    if debug:
        #print(letterSets)
        print(wrongPos)

    # Select a random word from the amended candidates list. Keep going until
    # we have a word that contains all the "gold" matches as well. Only repeat
    # for 'tries' times, in case conditions not satisfied.
    tries = 0
    while True:
        try:
            word = random.sample(candidates, 1)[0]
            tries += 1
        except Exception as err:
            if debug:
                print('****ERROR****')
                print(candidates)
                print(letterSets)
                print(wrongPos)
            return 'ERROR'

        if wrongPos.issubset(set(word)) or tries > 500:
            break

    if debug:
        print('\nCandidate words :', len(candidates))
        if len(candidates) < 30: print(candidates)
        print('New word selected :', word)

    return word

#-------------------------------------------------------------------------------

def matchWord(word, letterSets):
    """ Check if each letter in the word is present in the corresponding
        set of letters held in letterSets. Return True if found, else False. """

    for l1, l2 in zip(word, letterSets):
        if l1 not in l2:
            return False
    return True

#-------------------------------------------------------------------------------

def addNewWord(word):
    """ Add a new word to the csv word file and reload the dataframe. """

    with open('wordlist.csv', 'a', encoding='utf-8') as file:
        file.write('\n' + word)
    setupDataframe()

#-------------------------------------------------------------------------------

def main():
    """ Start point for this module, when run in isolation for testing.  """

    setupDataframe()
    temp = getSecretWord()
    print('Secret Word :', temp)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

#-------------------------------------------------------------------------------
