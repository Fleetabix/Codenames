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
			if wrd == "":
				continue
			if re.search(".*" + wrd, clue.lower()):
				return False
		
			if re.search(".*" + clue.lower(), wrd):
				return False
					
	
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
		input('\nPass to spymaster\n')

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

		return('pass', 1)
	
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
		self.old_clues = []

	def give_clue(self, currentGame):
		"""
			Returns the codeword and number of words to guess - always 3
		"""

		remaining_words = currentGame.wordCount(self.team)

		if (self.team == RED):
			results = []
			if remaining_words < 5:
				results = self.model.most_similar(
					positive = currentGame.redWords,
					negative = [currentGame.assassinWord]
				)
			else: 
				for i in range(0, remaining_words - 3):
					for j in range(i+1, remaining_words - 2):
						for k in range(j+1, remaining_words-1):
							for l in range(k+1, remaining_words):
								results += self.model.most_similar(
									positive = [
									currentGame.redWords[i],
									currentGame.redWords[j],
									currentGame.redWords[k],
									currentGame.redWords[l]
									],
									negative = [currentGame.assassinWord]
									)


		else:
			results = self.model.most_similar(
				positive = currentGame.blueWords,
				negative = [currentGame.assassinWord]
			)
	
		results.sort(key=lambda x:x[1], reverse=True)
		for word in results:
			if word[0] not in self.old_clues and self.valid_clue(currentGame.wordgrid, word[0]):
				guessnum = 4
				if remaining_words < 4:
					guessnum = remaining_words

				self.old_clues += word[0]	
				return (word[0], guessnum)
	




class Strategic_Gen_v2(Gen):

	def __init__(self, team):

		super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format(
			'components/models/GoogleNews-vectors-negative300.bin', 
			binary=True, 
			limit=100000
			)
		self.old_clues = []

	def give_clue(self, currentGame):
		"""
			Trys to find the most similar codeword across 2-5 words
		"""

		remaining_words = currentGame.wordCount(self.team)

		if (self.team == BLUE):
			results = []
			if remaining_words < 4:
				results = self.model.most_similar(
					positive = currentGame.blueWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			else: 
				for i in range(0, remaining_words - 2):
					for j in range(i+1, remaining_words - 1):
						for k in range(j+1, remaining_words):
						
							results += self.model.most_similar(
								positive = [
								currentGame.blueWords[i],
								currentGame.blueWords[j],
								currentGame.blueWords[k]
								],
								negative = [currentGame.assassinWord]
								)

				results = list(map(lambda x: (x, 3), results))


		else:
			results = []
			if remaining_words < 4:
				results = self.model.most_similar(
					positive = currentGame.redWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			else: 
				for i in range(0, remaining_words - 2):
					for j in range(i+1, remaining_words - 1):
						for k in range(j+1, remaining_words):
						
							results += self.model.most_similar(
								positive = [
								currentGame.redWords[i],
								currentGame.redWords[j],
								currentGame.redWords[k]
								],
								negative = [currentGame.assassinWord]
								)

				results = list(map(lambda x: (x, 3), results))

		results.sort(key=lambda x:x[0][1], reverse=True)
		#print(currentGame.blueWords)
		#print(results)
		for word in results:
			if word[0][0] not in self.old_clues and self.valid_clue(currentGame.wordgrid, word[0][0]):
				self.old_clues += word[0]
				return (word[0][0], word[1])



		return('pass', 1)

class Strategic_Gen_v3(Gen):

	def __init__(self, team):

		super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format(
			'components/models/GoogleNews-vectors-negative300.bin', 
			binary=True, 
			limit=100000
			)
		self.old_clues = []

	def give_clue(self, currentGame):
		"""
			Trys to find the most similar codeword across 2-5 words
		"""

		remaining_words = currentGame.wordCount(self.team)

		if (self.team == BLUE):
			results = []
			if remaining_words < 3:
				results = self.model.most_similar(
					positive = currentGame.blueWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			else: 
				for i in range(0, remaining_words - 1):
					for j in range(i+1, remaining_words):
										
						results += self.model.most_similar(
							positive = [
							currentGame.blueWords[i],
							currentGame.blueWords[j]
							],
							negative = [currentGame.assassinWord]
							)

				results = list(map(lambda x: (x, 2), results))


		else:
			results = []
			if remaining_words < 3:
				results = self.model.most_similar(
					positive = currentGame.redWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			else: 
				for i in range(0, remaining_words - 1):
					for j in range(i+1, remaining_words):
					
						results += self.model.most_similar(
							positive = [
							currentGame.redWords[i],
							currentGame.redWords[j]
							],
							negative = [currentGame.assassinWord]
							)

				results = list(map(lambda x: (x, 2), results))

		results.sort(key=lambda x:x[0][1], reverse=True)
		#print(currentGame.blueWords)
		#print(results)
		for word in results:
			if word[0][0] not in self.old_clues and self.valid_clue(currentGame.wordgrid, word[0][0]):
				self.old_clues += word[0]
				return (word[0][0], word[1])



		return('pass', 1)

class Automated_Gen_v2(Gen):
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
			results = self.model.most_similar_cosmul(
				positive = currentGame.redWords,
				negative = [currentGame.assassinWord]
			)

		else:
			results = self.model.most_similar_cosmul(
				positive = currentGame.blueWords,
				negative = [currentGame.assassinWord]
			)

		for word in results:
			if self.valid_clue(currentGame.wordgrid, word[0]):
				guessnum = 3
				if currentGame.wordCount(self.team) < 3:
					guessnum = currentGame.wordCount(self.team)
				return (word[0], guessnum)

		return('pass', 1)

class Strategic_Gen_v4(Gen):

	def __init__(self, team):

		super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format(
			'components/models/GoogleNews-vectors-negative300.bin', 
			binary=True, 
			limit=100000
			)
		self.old_clues = []

	def give_clue(self, currentGame):
		"""
			Trys to find the most similar codeword across 2-5 words
		"""

		remaining_words = currentGame.wordCount(self.team)

		if (self.team == BLUE):
			results = []
			if remaining_words < 4:
				results = self.model.most_similar_cosmul(
					positive = currentGame.blueWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			else: 
				for i in range(0, remaining_words - 2):
					for j in range(i+1, remaining_words - 1):
						for k in range(j+1, remaining_words):
						
							results += self.model.most_similar_cosmul(
								positive = [
								currentGame.blueWords[i],
								currentGame.blueWords[j],
								currentGame.blueWords[k]
								],
								negative = [currentGame.assassinWord]
								)

				results = list(map(lambda x: (x, 3), results))


		else:
			results = []
			if remaining_words < 4:
				results = self.model.most_similar_cosmul(
					positive = currentGame.redWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			else: 
				for i in range(0, remaining_words - 2):
					for j in range(i+1, remaining_words - 1):
						for k in range(j+1, remaining_words):
						
							results += self.model.most_similar_cosmul(
								positive = [
								currentGame.redWords[i],
								currentGame.redWords[j],
								currentGame.redWords[k]
								],
								negative = [currentGame.assassinWord]
								)

				results = list(map(lambda x: (x, 3), results))

		results.sort(key=lambda x:x[0][1], reverse=True)
		# print(currentGame.redWords)
		# print(results)
		for word in results:
			if word[0][0] not in self.old_clues and self.valid_clue(currentGame.wordgrid, word[0][0]):
				self.old_clues += word[0]
				return (word[0][0], word[1])



		return('pass', 1)

class Strategic_Gen_v5(Gen):

	def __init__(self, team):

		super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format(
			'components/models/GoogleNews-vectors-negative300.bin', 
			binary=True, 
			limit=100000
			)
		self.old_clues = []

	def give_clue(self, currentGame):
		"""
			Trys to find the most similar codeword across 2-5 words
		"""

		remaining_words = currentGame.wordCount(self.team)

		if (self.team == BLUE):
			results = []
			if remaining_words == 3:
				results = self.model.most_similar_cosmul(
					positive = currentGame.blueWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			elif remaining_words < 3:
				for i in range(0, remaining_words - 1):
					results += self.model.most_similar(
						positive = [currentGame.blueWords[i]],
						negative = [currentGame.assassinWord]
						)
				results = list(map(lambda x: (x, 1), results))
			else: 
				for i in range(0, remaining_words - 2):
					for j in range(i+1, remaining_words - 1):
						for k in range(j+1, remaining_words):
						
							results += self.model.most_similar_cosmul(
								positive = [
								currentGame.blueWords[i],
								currentGame.blueWords[j],
								currentGame.blueWords[k]
								],
								negative = [currentGame.assassinWord]
								)

				results = list(map(lambda x: (x, 3), results))


		else:
			results = []
			if remaining_words < 4:
				results = self.model.most_similar_cosmul(
					positive = currentGame.redWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			elif remaining_words < 3:
				for i in range(0, remaining_words - 1):
					results += self.model.most_similar(
						positive = [currentGame.redWords[i]],
						negative = [currentGame.assassinWord]
						)
				results = list(map(lambda x: (x, 1), results))
			else: 
				for i in range(0, remaining_words - 2):
					for j in range(i+1, remaining_words - 1):
						for k in range(j+1, remaining_words):
						
							results += self.model.most_similar_cosmul(
								positive = [
								currentGame.redWords[i],
								currentGame.redWords[j],
								currentGame.redWords[k]
								],
								negative = [currentGame.assassinWord]
								)

				results = list(map(lambda x: (x, 3), results))

		results.sort(key=lambda x:x[1], reverse=True)
		# print(currentGame.redWords)
		# print(results)
		for word in results:
			if word[0][0] not in self.old_clues and self.valid_clue(currentGame.wordgrid, word[0][0]):
				self.old_clues += word[0]
				return (word[0][0], word[1])



		return('pass', 1)

class Strategic_Gen_v6(Gen):

	def __init__(self, team):

		super().__init__(team)
		self.model = gensim.models.KeyedVectors.load_word2vec_format(
			'components/models/GoogleNews-vectors-negative300.bin', 
			binary=True, 
			limit=100000
			)
		self.old_clues = []

	def give_clue(self, currentGame):
		"""
			Trys to find the most similar codeword across 2-5 words
		"""

		remaining_words = currentGame.wordCount(self.team)

		if (self.team == BLUE):
			results = []
			if remaining_words == 3:
				results = self.model.most_similar_cosmul(
					positive = currentGame.blueWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			elif remaining_words < 3:
				results = self.model.most_similar(
					positive = currentGame.blueWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			else: 
				for i in range(0, remaining_words - 2):
					for j in range(i+1, remaining_words - 1):
						for k in range(j+1, remaining_words):
						
							results += self.model.most_similar_cosmul(
								positive = [
								currentGame.blueWords[i],
								currentGame.blueWords[j],
								currentGame.blueWords[k]
								],
								negative = [currentGame.assassinWord]
								)

				results = list(map(lambda x: (x, 3), results))


		else:
			results = []
			if remaining_words == 3:
				results = self.model.most_similar_cosmul(
					positive = currentGame.redWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			elif remaining_words < 3:
				results = self.model.most_similar(
					positive = currentGame.redWords,
					negative = [currentGame.assassinWord]
				)
				results = list(map(lambda x: (x, remaining_words), results))
			else: 
				for i in range(0, remaining_words - 2):
					for j in range(i+1, remaining_words - 1):
						for k in range(j+1, remaining_words):
						
							results += self.model.most_similar_cosmul(
								positive = [
								currentGame.redWords[i],
								currentGame.redWords[j],
								currentGame.redWords[k]
								],
								negative = [currentGame.assassinWord]
								)

				results = list(map(lambda x: (x, 3), results))

		results.sort(key=lambda x:x[0][1], reverse=True)
		# print(currentGame.redWords)
		# print(results)
		for word in results:
			if word[0][0] not in self.old_clues and self.valid_clue(currentGame.wordgrid, word[0][0]):
				self.old_clues += word[0]
				return (word[0][0], word[1])



		return('pass', 1)