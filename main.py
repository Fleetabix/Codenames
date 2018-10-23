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

	while True:
		takeTurn(BLUE, newGame)
		if newGame.checkWinner(BLUE) != 0:
			if newGame.checkWinner(BLUE) == BLUE:
				print('Blue team wins!')
			else:
				print('Red team wins!')
			break
		takeTurn(RED, newGame)
		if newGame.checkWinner(RED) != 0:
			if newGame.checkWinner(RED) == BLUE:
				print('Blue team wins!')
			else:
				print('Red team wins!')
			break
 

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
	clue = giveClue(BLUE, currentGame)

	print('The codeword is: {}\nThe number of words to guess is: {}'.format(clue[0], clue[1]))


	for i in range(1, clue[1]):
		guess = input('Please enter a word: ')

		while not currentGame.validGuess(guess):
			print('That word doesn\'t exist on the current board')
			guess = input('Please enter a word: ')

		outcome = currentGame.checkWord(guess)

		if outcome == team:
			print("Correct guess")
		elif outcome == ASSASSIN:
			print("Assasin found!")
			break
		elif outcome == CIV:
			print('Civilian detected')
			break
		else:
			print('Enemy spy detected!')
			break
		
def giveClue(team, currentGame):
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

# def switchTeam(team):
# 	"""
# 		Returns the opposite team
# 	"""

# 	if team == BLUE:
# 		return RED
# 	else
# 		return BLUE
	

if __name__ == '__main__':
	main()