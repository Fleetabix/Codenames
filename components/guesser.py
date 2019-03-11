from .gameboard import gameboard
import gensim
import random
import abc

class guesser:

	__metaclass__ = abc.ABCMeta

	def __init__(self):
		pass

	@abc.abstractmethod
	def guess(self, currentGame, guessword):
		pass

	

class Human_Guess(guesser):

	def __init__(self):
		pass


	def guess(self, currentGame, guessword):
		"""
			Ask for a word to be guessed
		"""

		guess = input('Please enter a word: ')

		while not currentGame.validGuess(guess):
			print('That word doesn\'t exist on the current board')
			guess = input('Please enter a word: ')

		return guess


class Random_Guess:
	"""
		A guesser that just randomly guesses words
	"""

	def __init__(self):
		pass

	def guess(self, currentGame, guessword):
		"""
			Randomly return a word from the wordgrid
		"""
		return random.choice(currentGame.wordgrid)



class Auto_Guess:
	"""
		A guesser that uses a model to choose the best guess on the board
	"""

	def __init__(self):

		self.model = gensim.models.KeyedVectors.load_word2vec_format('components/models/GoogleNews-vectors-negative300.bin', binary=True, limit=100000)


	def guess(self, currentGame, guessword):
		"""
			Choose highest match on remaining board
		"""
		matches = []

		for word in currentGame.wordgrid:
			matches.append((word, self.model.distance(guessword, word)))

		matches.sort(key=lambda x:x[1])

		return matches[0][0]