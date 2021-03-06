import time
import random
import AI

NUM_ANSWERS = 2315 # the number of valid answers (lines in valid_answers.txt)
NUM_GUESSES = 10657 # the number of valid guesses (lines in valid_guesses.txt)

# CLASS: QUORDLE
# represents a game of Wordle, quordle, or other.
# ARGS:
# answers - list of valid answers
# numWords - number of words for the game (1 for Wordle, 4 for Quordle, etc.)
class Quordle:
    def __init__(self, answers, numWords):
        self.answers = [] # list of hidden words
        self.numWords = numWords

        # randomly choose numWords number of hidden words
        i = 0
        while i < numWords:
            word = random.choice(answers)

            if word not in self.answers:
                self.answers.append(word)
                i += 1

    # FUNCTION: EVALUATE GUESS
    # takes a string guess and returns a string combination of G, Y, and B to
    # represent how good the guess was.
    # ARGS:
    # guess - the string an AI is guessing
    # RETURNS:
    # hints - list of strings made up of G Y and B to give back to AIs (possibly
    # more than one because in Quordle 4 different hints are returned for the
    # 4 different hidden words)
    def evaluateGuess(self, guess):
        hints = [] # list of hints to be returned.

        for answer in self.answers:
            hint = ''
            count = 0
            for letter in guess:
                if letter.lower() == answer[count]: # letter matches
                    hint += 'G'
                elif letter.lower() in answer: # letter in word but not that spot
                    hint += 'Y'
                else: # letter not in word
                    hint += 'B'

                count += 1
            hints.append(hint)
        return hints


def main():
    # Keeping track of time, do not want to make program too long.
    tic = time.time()

    # Create list of all possible answers (words that the hidden word could actually be)
    answers = []
    with open('data/valid_answers.txt') as answersText:
        answers = answersText.readlines()

    # Create list of all possible guesses (words that the AI can guess that will be accepted)
    guesses = []
    with open('data/valid_guesses.txt') as guessesText:
        guesses = guessesText.readlines()

    # Run tests on desired AI.
    # Change first arg for number of games
    # Change third arg for number of words in game (1 for wordle, 4 for quordle, etc)
    # Change last arg for the AI you want to test.
    res = PlayManyGames(100, answers, 4, AI.Entropy)
    print("\nAVERAGE NUM OF GUESSES: ", res[0], "\nWIN PERCENTAGE: ",
    res[1], "\nWORST GAME: ", res[2], "\nBEST GAME: ", res[3])

    # Report length of program
    toc = time.time()
    print("\nLENGTH OF PROGRAM", toc-tic, " seconds.")

# FUNCTION: PLAYAGAME
# Plays one singular game of wordle/quordle/other, and reports the number of
# guesses to get all of the words.
# ARGS:
# answers - valid answers
# numWords - number of words for the game (1 for Wordle, 4 for Quordle)
# ai - the AI type that we want to play
# RETURNS:
# numGuesses - the number of guesses needed to find the word.
def PlayAGame(answers, numWords, ai):
    game = Quordle(answers, numWords) # make new game
    myAI = ai(answers, numWords); # make new AI
    allGuesses = []
    numGuesses = 0
    numCorrect = 0
    print("--------------------------")

    print("\nHIDDEN WORDS ARE: ", game.answers)
    while numCorrect < numWords:
        word = myAI.pickWord() # AI picks a word
        numGuesses += 1
        print("PICKED WORD: ", word, " out of ", len(myAI.poolToChooseFrom)+1, " words")

        if word in game.answers: # exit if its correct (change for >1 word)
            numCorrect += 1
            allGuesses.append(word.upper())
        else:
            allGuesses.append(word)


        hint = game.evaluateGuess(word[:5]) # evaluate latest guess
        print(game.answers)
        print(hint)
        interpretationsCount = 0
        while interpretationsCount < numWords:
            myAI.interpretHint(hint[interpretationsCount], word[:5],
            myAI.guessPools[interpretationsCount]) # narrow down AI's guess pools
            print(interpretationsCount, ": ", len(myAI.guessPools[interpretationsCount]))
            interpretationsCount += 1
    print ("ALL GUESSES: ", allGuesses)
    print("GOT ALL WORDS IN :", numGuesses, " GUESSES.")
    print("--------------------------")
    return numGuesses


# FUNCTION: PLAYMANYGAMES
# Plays a particular number of games of wordle/quordle/other, and reports the
# number of guesses to get all of the words.
# ARGS:
# numGames - number of games we want the AI to play.
# answers - valid answers
# numWords - number of words for the game (1 for Wordle, 4 for Quordle)
# ai - the AI type that we want to play
# RETURNS:
# results - tuple with resulting average number of guesses, win percentage,
# the worst game the AI played, and the best game the AI played
def PlayManyGames(numGames, answers, numWords, ai):
    count = 0 # total number of guesses over all the games
    wins = 0 # number of times the AI guessed it in less than 6 (change for >1 word)
    best = 99 # best case, number should only go down
    worst = 0 # worst case, number should only go up
    goal = numWords + 5

    j = 0
    while j < numGames:
        newAnswers = answers.copy() # need to make new answers each time, otherwise
                                    # guessPools stay small.
        temp = PlayAGame(newAnswers, numWords, ai)
        if temp > worst: # updates worst if necessary.
            worst = temp
        if temp < best: # updates best if necessary.
            best = temp
        if temp <= goal: # adds a W if the AI won in time.
            wins += 1
        count += temp # update total number of guesses to calc avg later
        j += 1
        print("FINISHED GAME NUMBER: ", j)

    avg = count / numGames # find average
    winPct = wins / numGames # find win percentage
    return (avg, winPct, worst, best)

# FUNCTION: PERCENTAGEOFWORDS
# funcction i used to calculate the percentage of 5-letter words each letter
# is in.
def PercentageOfWords(words, letter):
    count = 0
    for word in words:
        if letter in word:
            count += 1
    return count / NUM_ANSWERS

# FUNCITON: PercentageOfLetters
# function i used to calculate the percentage of spots in the words with the certain
# letters are.
def PercentageOfLetters(words, letter, spot):
    count = 0
    for word in words:
        if letter == word[spot]:
            count += 1
    return count / NUM_ANSWERS


if __name__ == '__main__':
    main()
