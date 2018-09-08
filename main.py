#Entry point to the game
from components.gameboard import gameboard
import random

ERROR = -1
RED = 1
BLUE = 2
ASSASSIN = 3
CIV = 4


def main():
	"""
		Start a human vs human game
	"""
	wordfile = "components/srcWords.txt"

	wordgrid = createWord(wordfile)
	newGame = gameboard(wordgrid)

	print(newGame.currentBoard())

	takeTurn(BLUE, newGame)

def createWord(wordfile):
	"""
		Draw 25 random words to use in the game
	"""
	wordIndeces = random.sample(range(1, 400), 25)
	wordIndeces.sort()
	wordgrid = []

	j = 0
	with open(wordfile) as fp:
		for i, line in enumerate(fp):
			if j > 24:
				break
			elif i == wordIndeces[j]:
				wordgrid.append(line[:-1])
				j += 1
			
	return wordgrid




def takeTurn(team, currentGame):
	"""
		Allow a given team to take their turn
	"""
	print(currentGame.currentBoard())

	codeword = input('\nPlease type your codeword: ')
	
	while True :
		try:
			guessnum = int(input('Please type the number of words to guess: '))
			break
		except Exception as e:
			print('Must be a number')


	print('The codeword is: ', codeword)

	for i in range(1,guessnum):

		outcome = currentGame.checkWord(input('\nPlease type your guess: '))

		

	

if __name__ == '__main__':
	main()