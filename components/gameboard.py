#Generic gameboard
import random

ERROR = -1
RED = 1
BLUE = 2
ASSASSIN = 3
CIV = 4


class gameboard:
	"""
		Basic codenames gameboard that allows for a game to be played
	"""


	def __init__(self, wordgrid):
		self.wordgrid = wordgrid

		self.assignnment()

	def assignnment(self):
		"""
			Takes the shuffled wordgrid and assigns words to each category
		"""
		self.redWords = self.wordgrid[:7]
		self.blueWords = self.wordgrid[8:15]
		self.assassinWord = self.wordgrid[16]
		self.civWords = self.wordgrid[17:]

		random.shuffle(self.wordgrid)

	def checkWord(self, word):
		"""
			Takes a given word and determines if it is valid and if it exists returns which collection it belongs to
		"""
		
		self.wordgrid.remove(word)

		if word in self.redWords :
			self.redWords.remove(word)
			return RED
		elif word in self.blueWords :
			self.blueWords.remove(word)
			return BLUE
		elif word in self.assassinWord :
			return ASSASSIN
		else: 
			return CIV


	def validGuess(self, word):
		"""
			Takes a word and determines whether it still exists on the playing board
		"""

		if not word in self.wordgrid :
			return False
		else:
			return True


	def currentBoard(self):
		"""
			Outputs the current board scenario as a formatted string
		"""
		
		return 'Red: {}\nBlue: {}\nCivilians: {}\nAssassin: {}'.format(self.redWords, self.blueWords, self.civWords, self.assassinWord)


	def remainingWords(self):
		"""
			Returns the current board as a formatted string
		"""
		return self.wordgrid


	def checkWinner(self, team):
		"""
			Determines if a winner has been found from the current state of play
		"""
		if not self.redWords:
			return RED
		elif not self.blueWords:
			return BLUE
		elif not self.assassinWord:
			if team == BLUE:
				return RED
			else:
				return BLUE
		else:
			return 0 			

	def wordCount(self, team):
		"""
			Returns number of words remaining for a given team
		"""

		if team == RED :
			return len(self.redWords)
		else:
			return len(self.blueWords)


			