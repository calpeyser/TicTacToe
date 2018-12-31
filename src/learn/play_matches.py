import tensorflow as tf
import numpy as np
import random

from model import Q
from ..player import Player, RandomPlayer
from ..tictactoe import score, update_state, pretty_print_state, legal_moves, is_game_over, INITIAL_STATE

RANDOMIZATION_FACTOR = 0.03

def state_to_onehot(state):
	def box_to_onehot(box):
		if box == "":
			return [1, 0, 0]
		elif box == "X":
			return [0, 1, 0]
		elif box == "O":
			return [0, 0, 1]
		else:
			raise Exception("Invalid box value " + box)
	return [box_to_onehot(box) for box in state]

def argmax_for_indexes(soft, indexes):
	maxindex = 0
	maxvalue = float("-inf")
	for i, value in enumerate(soft):
		if i in indexes:
			if (value > maxvalue):
				maxindex = i
				maxvalue = value
	return maxindex

def model_move(soft_tensor, state_placeholder, sess):
	soft = sess.run(soft_tensor, {
		state_placeholder: state_onehot,
	})[0]
	predicted_move = argmax_for_indexes(soft, legal_moves(game_state))

class ModelPlayer(Player):
	def __init__(self, side, checkpoint_name, initialization_checkpoint):
		self.side = side
		self.checkpoint_name = checkpoint_name

		self.sess = tf.Session()
		with tf.variable_scope("model_" + checkpoint_name, reuse=tf.AUTO_REUSE) as scope:
			self.state_placeholder = tf.placeholder(tf.int32, shape=(9, 3))
			self.next_state_placeholder = tf.placeholder(tf.int32, shape=(9, 3))
			self.reward_placeholder = tf.placeholder(tf.int32)		
			self.soft_tensor, self.update_op, self.loss_op, self.reward_op= Q(self.state_placeholder,self.next_state_placeholder, self.reward_placeholder)
		self.saver = tf.train.Saver()
		if not initialization_checkpoint:
			self.sess.run(tf.global_variables_initializer())
		else:
			self.saver.restore(self.sess, "ckpt/" + initialization_checkpoint)

	def move(self, state):
		state_onehot = state_to_onehot(state)		
		soft = self.sess.run(self.soft_tensor, {
			self.state_placeholder: state_onehot,
		})[0]
		if random.random() > RANDOMIZATION_FACTOR:
			predicted_move = argmax_for_indexes(soft, legal_moves(state))
		else:
			predicted_move = random.choice(legal_moves(state))
		return predicted_move

	def update_model(self, state, new_state, reward):
		state_onehot = state_to_onehot(state)
		new_state_onehot = state_to_onehot(new_state)		
		loss, reward, _ = self.sess.run([self.loss_op, self.reward_op, self.update_op], {
			self.state_placeholder: state_onehot,
			self.next_state_placeholder: new_state_onehot,
			self.reward_placeholder: reward,
		})

	def save(self):
		self.saver.save(self.sess, "ckpt/"  + self.checkpoint_name)

class Counter(object):
	"""
	Keeps track of the number of games played, and their outcomes.
	"""

	def __init__(self, number_of_games_to_play):
		self.number_of_games_to_play = number_of_games_to_play
		self.games_played = 0
		self.opponent_win = 0
		self.model_win = 0
		self.ties = 0

	def game_over(self, final_state):
		PRINT = False
		self.games_played += 1
		reward = score(final_state)
		if reward == 5:
			if PRINT:
				print("model win")
				pretty_print_state(final_state)
			self.model_win += 1
		elif reward == -5:
			if PRINT:
				print("opponent_win")
				pretty_print_state(final_state)
			self.opponent_win += 1
		else:
			if PRINT:
				print("tie")
				pretty_print_state(final_state)
			self.ties += 1

	def all_games_have_been_played(self):
		return self.games_played >= self.number_of_games_to_play

	def summary(self):
		return float(self.model_win) / self.games_played, float(self.opponent_win) / self.games_played, float(self.ties) / self.games_played


def play_matches(opponent, model_player, number_of_games_to_play):
	old_state = None
	game_state = INITIAL_STATE

	#if not model_start_point:
	#	sess.run(tf.global_variables_initializer())
	#else: 
	#	saver.restore(sess, "ckpt/" + model_start_point)
	counter = Counter(number_of_games_to_play)
	while(not counter.all_games_have_been_played()):
		# Opponent move
		opponent_move = opponent.move(game_state)
		game_state = update_state(game_state, "X", opponent_move)
		if (is_game_over(game_state)):
			counter.game_over(game_state)
			game_state = INITIAL_STATE
			continue

		# Model move
		predicted_move = model_player.move(game_state)
		new_game_state = update_state(game_state, "O", predicted_move)
		new_state_onehot = state_to_onehot(new_game_state)
		reward = score(new_game_state)

		# Update model
		model_player.update_model(game_state, new_game_state, reward)
		if (is_game_over(new_game_state)):
			counter.game_over(new_game_state)
			old_state = None
			game_state = INITIAL_STATE
			continue
		else:
			old_state = game_state
			game_state = new_game_state
	model_player.save()
	return counter.summary(), 


if __name__=="__main__":
	play_matches(RandomPlayer("X"), None, "model0", 100)

