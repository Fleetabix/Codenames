from gameboard import gameboard
import gensim
ERROR = -1
RED = 1
BLUE = 2
ASSASSIN = 3
CIV = 4


class Human_Gen:
	"""
	A human guesser class - doesn't store any info
	"""
	def __init__(self):
		
		

	def giveClue(self, team, currentGame):
		"""
			Returns the codeword and a number of words to guess
		"""

		print(currentGame.currentBoard())
		codeword = input('\nPlease type your codeword: ')
		
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


class Automated_Gen:
	"""
	docstring for Automated_Generator
	"""
	def __init__(self):
		
		self.model = gensim.models.KeyedVectors.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True, limit=50000)

	def giveClue(self, team, currentGame):
		"""
			Returns the codeword and number of words to guess - always 3
		"""
		if (team == RED):
			results = self.model.most_similar(
				positive = currentGame.redWords[:3],
				negative = currentGame.assassinWord
			)

		else:
			results = self.model.most_similar(
				positive = currentGame.blueWords[:3],
				negative = currentGame.assassinWord
			)


		return (results[0][0], 3)