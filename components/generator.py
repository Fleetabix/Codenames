from .gameboard import gameboard
import gensim

class Gen:
	"""A general guesser class"""
	ERROR = -1
	RED = 1
	BLUE = 2
	ASSASSIN = 3
	CIV = 4



	def __init__(self, team):
		self.team = team

	def valid_guess(self, words, guess):
		return True

	@abstractmethod
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

		print(currentGame.currentBoard())
		
		while True:

			codeword = input('\nPlease type your codeword: ')

			if self.valid_guess(codeword) :
				break
			else :
				print("Not a valid codeword!")


		while True :
			try:
				guessnum = int(input('Please type the number of words to guess: '))
			except Exception as e:
				print('Must be a number')	
			
			if guessnum > 0 and guessnum <= currentGame.wordCount(team):
				break
			else:
				print("Number can only be less than remaining words")

		return (codeword, guessnum)


class Automated_Gen(Gen):
	"""
	docstring for Automated_Generator
	"""
	def __init__(self, team):

		self.super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True, limit=50000)

	def give_clue(self, currentGame):
		"""
			Returns the codeword and number of words to guess - always 3
		"""
		if (self.team == RED):
			results = self.model.most_similar(
				positive = currentGame.redWords[:3],
				negative = currentGame.assassinWord
			)

		else:
			results = self.model.most_similar(
				positive = currentGame.blueWords[:3],
				negative = currentGame.assassinWord
			)

		for word in results:
			if self.valid_guess(word[0]):
				return (word[0], 3)


class Chaos_Gen(Gen):
	"""docstring for Chaos_Gen"""
	def __init__(self, team):
		super().__init__(team)
		
	def give_clue(self, currentGame):
		return ("", currentGame.wordCount(team))

		