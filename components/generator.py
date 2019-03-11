from .gameboard import gameboard
import gensim
import abc
import re

ERROR = -1
RED = 1
BLUE = 2
ASSASSIN = 3
CIV = 4

class Gen:
	"""A general guesser class"""

	__metaclass__ = abc.ABCMeta

	

	
	def __init__(self, team):
		
		self.team = team

	@staticmethod
	def valid_clue(words, clue):
		if re.search("^DBPEDIA", clue) :
			return False

		
		
		for wrd in words:
			if re.search("^" + wrd, clue.lower()):
				return False
				try:
					if re.search("^" + clue.lower(), wrd):
						return False
					
				except Exception as e:
					print(clue)
					raise e
	
		return True

	@abc.abstractmethod
	def give_clue(self, currentGame):
		pass


class Human_Gen(Gen):
	"""
	A human guesser class - doesn't store any info
	"""
	def __init__(self, team):
		super().__init__(team)


	def give_clue(self, currentGame):
		"""
			Returns the codeword and a number of words to guess
		"""
		input('\nPass to guesser\n')

		print(currentGame.currentBoard())
		
		while True:

			codeword = input('\nPlease type your codeword: ')

			if self.valid_clue(currentGame.wordgrid, codeword) :
				break
			else :
				print("Not a valid codeword!")


		while True :
			try:
				guessnum = int(input('Please type the number of words to guess: '))

				if guessnum > 0 and guessnum <= currentGame.wordCount(self.team):
					break
				else:
					print("Number can only be less than remaining words")
			except Exception as e:
				print('Must be a number')	
							

		return (codeword, guessnum)




class Chaos_Gen(Gen):
	"""
	Just returns blank clues with maximum word count - maximum unhelpfulness
	"""
	def __init__(self, team):
		super().__init__(team)
		
	def give_clue(self, currentGame):
		"""
		Gives an empty clue, but highest possible number of words
		"""
		return ("", currentGame.wordCount(self.team))

class Automated_Gen(Gen):
	"""
	docstring for Automated_Generator
	"""
	def __init__(self, team):

		super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format(
			'components/models/GoogleNews-vectors-negative300.bin', 
			binary=True, 
			limit=100000
			)

	def give_clue(self, currentGame):
		"""
			Returns the codeword and number of words to guess - always 3
		"""
		if (self.team == RED):
			results = self.model.most_similar(
				positive = currentGame.redWords,
				negative = [currentGame.assassinWord]
			)

		else:
			results = self.model.most_similar(
				positive = currentGame.blueWords,
				negative = [currentGame.assassinWord]
			)

		for word in results:
			if self.valid_clue(currentGame.wordgrid, word[0]):
				guessnum = 3
				if currentGame.wordCount(self.team) < 3:
					guessnum = currentGame.wordCount(self.team)
				return (word[0], guessnum)
	
class Wiki_Gen(Gen):

	def __init__(self, team):
		super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format(
			'components/models/wiki_model.bin', 
			binary=True,
			limit=100000
			)

	def give_clue(self, currentGame):

		if (self.team == RED):
			results = self.model.most_similar(
				positive = currentGame.redWords,
				negative = [currentGame.assassinWord]
			)

		else:
			results = self.model.most_similar(
				positive = currentGame.blueWords,
				negative = [currentGame.assassinWord]
			)

		for word in results:
			if self.valid_clue(currentGame.wordgrid, word[0].rstrip(')')):
				guessnum = 3
				if currentGame.wordCount(self.team) < 3:
					guessnum = currentGame.wordCount(self.team)
				return (word[0].rstrip(')'), guessnum)

class Strategic_Gen(Gen):

	def __init__(self, team):

		super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format(
			'components/models/GoogleNews-vectors-negative300.bin', 
			binary=True, 
			limit=100000
			)

	def give_clue(self, currentGame):
		"""
			Returns the codeword and number of words to guess - always 3
		"""

		remaining_words = currentGame.wordCount(self.team)

		if (self.team == RED):

			if remaining_words < 5:
				results = self.model.most_similar(
					positive = currentGame.redWords,
					negative = [currentGame.assassinWord]
				)
			else: 
				for i in range(0, remaining_words - 4):
					pass







		else:
			results = self.model.most_similar(
				positive = currentGame.blueWords,
				negative = [currentGame.assassinWord]
			)

		for word in results:
			if self.valid_clue(currentGame.wordgrid, word[0]):
				guessnum = 4
				if remaining_words < 4:
					guessnum = remaining_words
				return (word[0], guessnum)