import tensorflow as tf
import random

class Player():
	def __init__(self, side):
		self.side = side

	def move(self, state):
		pass

class RandomPlayer(Player):
	def move(self, state):
		possible_moves = []
		for i in range(9):
			if not state[i]:
				possible_moves.append(i)
		return random.choice(possible_moves)
