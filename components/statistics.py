ERROR = -1
RED = 1
BLUE = 2
ASSASSIN = 3
CIV = 4

class game_stats():
	"""
		Records statistics for the duration of the game
	"""
	def __init__(self):
		self.red_wins = 0
		self.blue_wins = 0
		self.round_counter = 0
		self.game_summary = []

	def new_round(self):

		self.round_counter += 1


	def new_game(self, start_team):

		self.round_counter = 0
		
		self.game_summary.append({
			'start_team' : start_team,
			'is_assassin' : False
		})

	def assassin_detected(self):

		self.game_summary[-1]['is_assassin'] = True

	def end_game(self, winner, true_win):

		self.game_summary[-1].update({
			'rounds' : self.round_counter,
			'winner' : winner,
			'true_win' : true_win
		})
		if winner == BLUE:
			self.blue_wins += 1
		else:
			self.red_wins += 1
			

	def summary_stats(self):
		return "Rounds played: {}\nBlue wins: {}\nRed wins: {}".format(
			len(self.game_summary),
			self.blue_wins,
			self.red_wins
		)

	def export_stats(self):
		pass