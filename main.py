#Entry point to the game
from components.gameboard import gameboard
from components.generator import *
from components.guesser import *
from components.statistics import game_stats

import random
import os
import sys


ERROR = -1
RED = 1
BLUE = 2
ASSASSIN = 3
CIV = 4

stat_collector = game_stats()


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
	elif sys.argv[1] == '6':
		players = Players(
			News_Guess(),
			News_Guess(),
			Automated_Gen(RED),
			Strategic_Gen_v2(BLUE)
			)
	elif sys.argv[1] == '7':
		players = Players(
			News_Guess(),
			News_Guess(),
			Automated_Gen(RED),
			Strategic_Gen_v3(BLUE)
			)
	elif sys.argv[1] == '8':
		players = Players(
			News_Guess(),
			News_Guess(),
			Automated_Gen(RED),
			Automated_Gen_v2(BLUE)
			)
	elif sys.argv[1] == '9':
		players = Players(
			News_Guess(),
			News_Guess(),
			Automated_Gen(RED),
			Strategic_Gen_v4(BLUE)
			)
	try: 
		rounds = int(sys.argv[2])
	except Exception as e:
		rounds = 1

	red_wins = 0
	blue_wins = 0

	if random.random() > 0.5 :
		start_team = BLUE
	else :
		start_team = RED

	for x in range(0, rounds):
		
		playGame(players, start_team) == RED
			
		start_team = switchTeam(start_team)

	print(stat_collector.summary_stats())

	stat_collector.export_stats()


def playGame(players, active_team):
	"""
		Start a game, given team goes first
	"""
	wordfile = "components/easyWords.txt"

	
	wordgrid = createWord(wordfile)
	newGame = gameboard(wordgrid)
	#os.system('clear')

	stat_collector.new_game(active_team)

	while True:

		stat_collector.new_round()

		if active_team == RED:
			
			print('Blue team goes!')
			takeTurn(BLUE, players, newGame)
			checkWinner = newGame.checkWinner(BLUE)
			if checkWinner ==  BLUE:
				stat_collector.end_game(BLUE, True)
				print('Blue team wins!')
				return BLUE
			elif checkWinner == RED:
				stat_collector.end_game(RED, False)
				print('Red team wins!')
				return RED

		else:

			print('Red team goes!')
			takeTurn(RED, players, newGame)
			checkWinner = newGame.checkWinner(RED)
			if checkWinner ==  BLUE:
				stat_collector.end_game(BLUE, False)
				print('Blue team wins!')
				return BLUE
			elif checkWinner == RED:
				stat_collector.end_game(RED, True)
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

	if clue == None:
		return

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
			stat_collector.assassin_detected()
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



