import tensorflow as tf

TD_RATE = 0.08
LEARNING_RATE = 0.08

def make_net(input):
	net = tf.layers.dense(input, 1)
	net = tf.transpose(net, perm = [1, 0])
	net = tf.layers.dense(net, 128)
	net = tf.layers.dense(net, 128)
	net = tf.layers.dense(net, 9)
	return net

def Q(state, next_state, reward):
	state = tf.cast(state, tf.float32)
	next_state = tf.cast(next_state, tf.float32)
	reward = tf.cast(reward, tf.float32)

	Q_net = make_net(state)
	Q_soft = tf.nn.softmax(Q_net)
	Q_best_soft = tf.reduce_max(Q_soft)

	TD_net = make_net(next_state)
	TD_soft = tf.nn.softmax(TD_net)
	TD_best_soft = tf.reduce_max(TD_soft)

	TD_criterion = tf.multiply(TD_RATE, tf.math.square(tf.subtract(TD_best_soft, Q_best_soft)))
	loss = tf.add(reward, TD_criterion)
	update_op = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(loss)

	return Q_soft, update_op, TD_soft, reward
