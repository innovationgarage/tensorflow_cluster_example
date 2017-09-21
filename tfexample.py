import tensorflow as tf

with tf.Session('grpc://localhost:4711') as s:
    with tf.device("/job:worker"):
        node1 = tf.constant(3.0, dtype=tf.float32)
        node2 = tf.constant(5.0, dtype=tf.float32)
        node3 = tf.add(node1, node2)
    print s.run(node3)
