#Entry point to the game
from components.gameboard import gameboard

ERROR = -1
RED = 1
BLUE = 2
ASSASSIN = 3
CIV = 4

def main():
	"""
		Start a human vs human game
	"""
	wordgrid = list(map(chr, range(97, 122)))
	newGame = gameboard(wordgrid)

	print(newGame.currentBoard())

	takeTurn(BLUE, newGame)

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

	for i in range(1,10):

		outcome = currentGame.checkWord(input('\nPlease type your guess: '))

		if :
			pass
		

	

if __name__ == '__main__':
	main()