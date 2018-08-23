#Entry point to the game
from components.gameboard import gameboard



def main():
	"""
		Start a human vs human game
	"""
	wordgrid = list(map(chr, range(97, 122)))
	newGame = gameboard(wordgrid)

	print(newGame.currentBoard())


if __name__ == '__main__':
	main()