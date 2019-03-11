#Entry point to the game
from components.gameboard import gameboard
from components.generator import *
from components.guesser import *

import random
import os
import sys


ERROR = -1
RED = 1
BLUE = 2
ASSASSIN = 3
CIV = 4

class Players:

	def __init__(self, red_guesser, blue_guesser, red_gen, blue_gen):

		self.red_guesser = red_guesser
		self.blue_guesser = blue_guesser
		self.red_gen = red_gen
		self.blue_gen = blue_gen


def main():
	"""
		Create guessers and generators
	"""
	print(sys.argv[1]) 	
	if sys.argv[1] == '1':
		players = Players(
		Human_Guess(),
		Human_Guess(),
		Human_Gen(RED),
		Human_Gen(BLUE)
		)
	elif sys.argv[1] == '2':
		players = Players(
		Human_Guess(),
		Human_Guess(),
		Human_Gen(RED),
		Automated_Gen(BLUE)
		)
	elif sys.argv[1] == '3':
		players= Players(
		Human_Guess(),
		Human_Guess(),
		Strategic_Gen(RED),
		Human_Gen(BLUE)
		)
	elif sys.argv[1] == '4':
		players = Players(
			News_Guess(),
			Random_Guess(),
			Automated_Gen(RED),
			Chaos_Gen(BLUE)
			)
	elif sys.argv[1] == '5':
		players = Players(
			News_Guess(),
			Wiki_Guess(),
			Automated_Gen(RED),
			Wiki_Gen(BLUE)
			)
		
	rounds = 1
	try: 
		rounds = int(sys.argv[2])
	except Exception as e:
		pass

	red_wins = 0
	blue_wins = 0

	if random.random() > 0.5 :
		start_team = BLUE
	else :
		start_team = RED

	for x in range(0, rounds):
		
		if playGame(players, start_team) == RED :
			red_wins += 1
		else:
			blue_wins += 1

		start_team = switchTeam(start_team)

	print('Rounds played: {}\nRed wins: {}\nBlue wins: {}'.format(rounds, red_wins, blue_wins))



def playGame(players, active_team):
	"""
		Start a game, given team goes first
	"""
	wordfile = "components/easyWords.txt"

	
	wordgrid = createWord(wordfile)
	newGame = gameboard(wordgrid)
	#os.system('clear')
	while True:
		if active_team == RED:
			
			print('Blue team goes!')
			takeTurn(BLUE, players, newGame)
			checkWinner = newGame.checkWinner(BLUE)
			if checkWinner ==  BLUE:
				print('Blue team wins!')
				return BLUE
			elif checkWinner == RED:
				print('Red team wins!')
				return RED

		else:

			print('Red team goes!')
			takeTurn(RED, players, newGame)
			checkWinner = newGame.checkWinner(RED)
			if checkWinner ==  BLUE:
				print('Blue team wins!')
				return BLUE
			elif checkWinner == RED:
				print('Red team wins!')
				return RED

		active_team = switchTeam(active_team)


def createWord(wordfile):
	"""
		Draw 25 random words to use in the game
	"""
	wordIndeces = random.sample(range(1, 346), 25)
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




def takeTurn(team, players, currentGame):
	"""
		Allow a given team to take their turn
	"""
	
	

	
	print(currentGame.remainingWords())
	
	if team == RED:
		clue = players.red_gen.give_clue(currentGame)
	else:
		clue = players.blue_gen.give_clue(currentGame)

	os.system('clear')

	print('The codeword is: {}\nThe number of words to guess is: {}'.format(clue[0], clue[1]))

	for i in range(0, clue[1]):
		


		print(currentGame.remainingWords())
		if team == RED:
			guess = players.red_guesser.guess(currentGame, clue[0])
		else:
			guess = players.blue_guesser.guess(currentGame, clue[0])

		print('Guess was:{}'.format(guess))
		outcome = currentGame.checkWord(guess.lower())


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
		


def switchTeam(team):
	"""
		Returns the opposite team
	"""

	if team == BLUE:
		return RED
	else :
		return BLUE
	

if __name__ == '__main__':

	if len(sys.argv) < 2 :
		print('Please specify type of game:')
		print('1 - Human vs Human game')
		print('2 - Human vs Computer game')
		print('3 - Computer vs Computer game')
		print('4 - ')
	else :
		main()



