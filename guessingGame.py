""" 
# =============================================================================
# Author: OctraSource
# Description: A game where you guess the index of where a movie is in a shuffled list.
# Input:
    The number of movies you want to guess (int)
    The difficulty of your current playsession (int)
    The list of movies (str), repeated for however many movies you entered for the first input
    The index you're guessing when prompted with a movie name (int), repeated for however many movies you entered for the first input

# Ouput:
    Error messages that help the user and specify what's needed
    A notification telling you how many points you have and how many you need to win after specifying a difficulty
    -- repeated for however many movies you have --
        Your list of movies
        A shuffle notification
        Your current points and how many are needed to win
        A hint telling you which indexes can't be the index of this movie (from previous attempts)
        Whether or not you guessed the index correctly
    -- --
    Whether or not you won or lost, and how many points you ended with
    The list that was shuffled
# =============================================================================
"""

import random
import os
import time


"""
    game(startingPoints, numberOfMovies, awardPoints, passingPoints)
        "startingPoints" is the amount of points the player starts with
        "numberOfMovies" is the number of movies the user wants to guess
        "awardPoints" is the number of points a player is rewarded or penalized with 
        "passingPoints" is the number of points a player can have to win the game

    the game!
    contains the list of movies, the number of points the player is award/penalized with, the number of points to win, as well as the amount of starting points for the player.
    also contains the player themself and several methods for getting the values above as well as a method to shuffle the current list.
"""
class game():

    # runs upon the game object being created
    def __init__(self, startingPoints, numberOfMovies, awardPoints = 100):
        self.setMovieCount(numberOfMovies)
        self.setAnswerReward(awardPoints)

        # sets the passing points to whatever the user sets the difficulty to (difficulty of 1 means they have 100 passing points)
        self.setPassingPoints(100 * getInput(f"Enter the difficulty from 1 (100 points needed to win) to {numberOfMovies} ({numberOfMovies*100} points needed to win): ", numberOfMovies, f"Enter a number between 1 and {numberOfMovies}!", 1))


        # create the player
        self.createPlayer(self.player(startingPoints))
        print(f"you will need to have {self.getPassingPoints()} to win.")

        cleanTerminal(5)

        self.setMovies(self.createMoviesList())

        cleanTerminal(0)
        
    """
        player(startingPoints)
            "startingPoints" is the amount of points this player starts with.

        the player!
        contains the player's current points as well as methods to modify said points.
    """
    class player():

        # runs upon the player object being created
        def __init__(self, startingPoints):
            print(f"You will be starting with {self.setPoints(startingPoints)} points, and ", end = "")

        # when the object is casted as a string, return what's specified
        def __str__(self):
            return f"You have {self.getPoints()} points!"
        
        # returns the points the player currently has
        def getPoints(self):
            return self.points
        
        # sets the points to a specified value. returns the new points.
        def setPoints(self, value):
            self.points = value
            return value
        
        # reduces the points by a specified value. returns the new points.
        def addPoints(self, amount):
            return self.setPoints(self.getPoints() + amount)
        

    # returns the number of points needed to win the game
    def getPassingPoints(self):
        return self.passingPoints
    
    # sets the number of points needed to win the game and returns that new value
    def setPassingPoints(self, value):
        self.passingPoints = value
        return value
    
    # creates a player into the game and returns that new player
    def createPlayer(self, player):
        self.curPlayer = player
        return player
    
    # returns the current player object who's playing the game
    def getCurrentPlayer(self):
        return self.curPlayer
    

    # sets the current number of movies and returns the value you set it to
    def setMovieCount(self, value):
        self.movieCount = value
        return value
    
    # returns the number of movies
    def getMovieCount(self):
        return self.movieCount
    
    # sets the number of points a player is rewarded after answering correctly and returns the value you set it to
    def setAnswerReward(self, value):
        self.answerReward = value
        return value
    
    # returns the number of points a player is rewarded after answering correctly
    def getAnswerReward(self):
        return self.answerReward


    # returns the list of movies
    def getMovies(self):
        return self.moviesList
    
    # sets the current list of movies to what you pass and returns the list you passed
    def setMovies(self, newMovies):
        self.moviesList = newMovies
        return self.moviesList
    
    # creates and returns the list of movies via user input
    def createMoviesList(self):
        arr = []

        # prompts the user for movie names for however many they wanted to do
        for i in range(0, self.getMovieCount(), 1):
            arr.append(input(f"Enter a movie name ({i+1}): "))

        return arr    
    
    # returns a shuffled list of movies
    def shuffleMovies(self):
        curList = self.getMovies()
        newList = []

        while len(newList) != self.getMovieCount():
            curIndex = roundRandomFairly(0, len(curList) - 1)

            newList.append(curList[curIndex])

            del curList[curIndex]

        self.setMovies(newList)
        print("List shuffled!")
        return self.getMovies()
    

    # plays the game!
    def playGame(self):
        movieCount = self.getMovieCount()
        activePlayer = self.getCurrentPlayer()
        reward = self.getAnswerReward()
        pointsToPass = self.getPassingPoints()

        originalList = cleanList(self.getMovies())

        currentMovieList = self.shuffleMovies()
    
        # a list of indexes of movies we shouldn't repeat
        excludeIndex = []

        # repeat "movieCount" number of times
        for i in range(0, movieCount, 1):
            print(f"Your list of movies is: {originalList}")
            print(f"\n{str(activePlayer)} You need at least {pointsToPass} to win!\n")

            # print(f"the shuffled list is: {currentMovieList}") # uncomment this if you're cheating (or debugging)! prints the shuffled list

            actualIndex = roundRandomFairly(0, movieCount - 1, excludeIndex)

            # if we have previously got a guess and have an excluded value,
            if excludeIndex:
                # notify the user
                print(f"Hint: current indexes can't be: {cleanList(excludeIndex)}")

            # get the player's index guess
            playerSelection = getInput(f"Guess the index for the movie '{currentMovieList[actualIndex]}' from 0 to {movieCount - 1}!: ", 
                                       movieCount - 1, f"Enter an index from 0 to {movieCount - 1}!")

            # if the player was right,
            if playerSelection == actualIndex:
                # player should be rewarded
                activePlayer.addPoints(reward)
                print("Correct! (+100 points)")
            # if they weren't,
            else:
                # player should be penalized
                activePlayer.addPoints(-reward)
                print("Sorry, incorrect! (-100 points)")
                print(f"This movie was at index {actualIndex}.")

            cleanTerminal(5)

            # make sure we don't prompt the user this same movie again
            excludeIndex.append(actualIndex)

        # if the player didn't pass,
        if activePlayer.getPoints() < pointsToPass:
            # notify them they lost
            print(f"You lost! {str(activePlayer)} You needed {pointsToPass} to win!")
        # if they did,
        else:
            # notify them they won
            print(f"You won! {str(activePlayer)} Congratulations!")

        # provide them the shuffled list
        print(f"The shuffled list was: {cleanList(currentMovieList)}\nYour original list was: {originalList}")


"""
    getInput(question, gettingMovies, maximum, error)
        "question" is the prompt the user sees before an input is triggered
        "maximum" specifies the largest value the user can input. if not passed, then this is assuming the function is getting movie names and not a number
        "error" is the error the user sees when they input something incorrectly

    If "maximum" is set to a number, the user must enter a number between and including 0 and the "maximum". The value they enter is returned if this condition is met.
    If "maximum" is not set to a value, then this function will return a number the user enters only when it is greater than 1.
"""
def getInput(question, maximum = None, error = "Enter a number greater than 1!", minimum = 0):
    try:
        # the user's response to the question "question"
        response = int(input(question))

        # if we're getting the number of movies (maximum exists), the response they enter must be greater than 1
        if maximum:
            # if the response the user gave is less than the minimum or greater than the maximum,
            if not(response >= minimum and response <= maximum):
                # throw an error
                raise(Exception("Out of range!"))
        # otherwise, just check if it's greater than 1. if it is less than 1,
        elif not(response > 1):
            # throw an error
            raise(Exception("Invalid number!"))
        
        return response
    except:
        print(error)
        return getInput(question, maximum, error, minimum)
    

"""
    roundRandomFairly(low, high, exclusion)
        "low" is the lowest integer value the random integer can be
        "high" is the highest integer value the random integer can be
        "exclusion" is a list of numbers the random integer CAN'T be. doesn't have to be set
    
    returns a random integer from "low" to "high" that is NOT in "exclusion".
    rounding normally will always round DOWN, but this function allows us to round up if the number we create has a decimal greater than or equal to .5
"""
def roundRandomFairly(low, high, exclusion = None):
    # the random value we generated from high to low
    randValue = (random.random() * high) + low

    # if the value has a decimal greater than or equal to .5, then casting this will round it upwards. otherwise, it'll just stay to what it used to be.
    fairRound = int(randValue + .5)

    # if we're excluding values, check if the number we rounded is in the excluded list
    if exclusion and fairRound in exclusion:
        # if the number we generated is an excluded value, generate a number again
        return roundRandomFairly(low, high, exclusion)
    
    # if the number isn't in the list, then just return it
    return fairRound



"""
    cleanTerminal()
    
    clears the spyder and vscode terminal
"""
def cleanTerminal(wait):
    # pause for "wait" seconds
    time.sleep(wait)

    # clean vscode terminal
    os.system("cls||clear")
    # clean spyder terminal
    print("\033[H\033[J")


"""
    cleanList(arr)
        "arr" is a list

    returns a string of "arr" without its brackets
"""
def cleanList(arr):
    return str(arr).strip('[').strip(']')


"""
    The glorious main function!
"""
if __name__ == "__main__":
    currentInputs = 0

    totalMovies = getInput("Enter the number of movies you'd like to guess: ")
    startingPoints = totalMovies * 100

    session = game(startingPoints, totalMovies)

    session.playGame()