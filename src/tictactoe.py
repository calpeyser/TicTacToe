INITIAL_STATE = ["", "", "", "", "", "", "", "", ""]

LINES = [
	[0, 1, 2],
	[3, 4, 5],
	[6, 7, 8],
	[0, 3, 6],
	[1, 4, 7],
	[2, 5, 8],
	[0, 1, 2],
	[2, 4, 6],
]

def is_game_over(state):
	if score(state) != 0:
		return True
	if not [pos for pos in range(8) if state[pos] == ""]:
		return True
	return False

def score(state):
	"""
	Returns:
		1 if O wins
		-1 if X wins
		0 if nether side has won yet, or on a draw
	"""
	for line in LINES:
		if [state[pos] for pos in line] == ["O", "O", "O"]:
			return 5
		elif [state[pos] for pos in line] == ["X", "X", "X"]:
			return -5
	return 0

def update_state(state, player, move):
	"""
	Returns the state after the given move.
	"""
	if state[move] != "":
		raise Exception("Illegal move: " + player + " moves " + str(move) + " with state " + str(state))
	new_state = list(state)
	new_state[move] = player
	return new_state

def legal_moves(state):
	return [move for move in range(9) if state[move] == ""]

def pretty_print_state(state):
	print (
		"""
%s | %s | %s
------------
%s | %s | %s
------------
%s | %s | %s
		""" % (state[0], state[1], state[2], state[3], state[4],
			   state[5], state[6], state[7], state[8]))