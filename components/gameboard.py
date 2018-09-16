#Generic gameboard



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
		self.blueWords = self.wordgrid[8:14]
		self.assassinWord = self.wordgrid[15]
		self.civWords = self.wordgrid[16:]

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
		else : 
			return CIV


	def validGuess(self, word):
		"""
			Takes a word and determines whether it still exists on the playing board
		"""

		if not word in self.wordgrid :
			return false
		else
			return true


	def currentBoard(self):
		"""
			Outputs the current board scenario as a formatted string
		"""
		
		return 'Red: {}\nBlue: {}\nCivilians: {}\nAssassin: {}'.format(self.redWords, self.blueWords, self.civWords, self.assassinWord)


	def checkWinner(self):
		"""
			Determines if a winner has been found from the current state of play
		"""
		if not self.redWords:
			return RED
		elif not self.blueWords:
			return BLUE 

	def wordCount(self, team):
		"""
			Returns number of words remaining for a given team
		"""

		if team == RED :
			return redWords.len()
		else
			return blueWords.len()


			