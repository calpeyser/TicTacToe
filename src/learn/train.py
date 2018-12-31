from play_matches import play_matches, ModelPlayer
from ..player import RandomPlayer

if __name__=="__main__":

	opponent = RandomPlayer("X")
	model_num = 1
	model = None
	first_round = False
	for i in range(5000):
		last_model_ckpt = "model_" + str(model_num - 1)
		model_ckpt = "model_" + str(model_num)
		if i == 0:
			initialization_checkpoint = None
		elif first_round:
			first_round = False
			initialization_checkpoint = last_model_ckpt
		else:
			initialization_checkpoint = model_ckpt
		model_player = ModelPlayer("O", model_ckpt, initialization_checkpoint)			
		prop = play_matches(opponent, model_player, 1000)
		print("%s %s" % (str(prop), "Generation " + str(model_num)))
		if prop[0][0] > prop[0][1]:
			first_round = True
			opponent = ModelPlayer("O", model_ckpt, model_ckpt)
			model_num += 1



