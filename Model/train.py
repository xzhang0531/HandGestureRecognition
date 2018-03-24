import tensorflow as tf
import numpy as np
import tflearn
from tflearn.data_utils import shuffle, to_categorical

data1 = np.loadtxt('resizedData_1.txt',delimiter=', ')
data1 = data1.reshape(100,10000)
data2 = np.loadtxt('resizedData_2.txt',delimiter=', ')
data2 = data2.reshape(100,10000)
data3 = np.loadtxt('resizedData_3.txt',delimiter=', ')
data3 = data3.reshape(100,10000)
data = np.concatenate((data1, data2, data3))


label1 = []
label2 = []
label3 = []
for i in range(100):
	label1.append(0)
	label2.append(1)
	label3.append(2)

label1 = np.array(label1)
label2 = np.array(label2)
label3 = np.array(label3)
label = np.concatenate((label1, label2, label3))
label = to_categorical(label,3)


idx = np.arange(0, len(data))
np.random.shuffle(idx)
idxtest = idx[0:50]
idxtrain = idx[50:300]
data_test = [data[i] for i in idxtest]
data_test = np.asarray(data_test)
label_test = [label[i] for i in idxtest]
label_test = np.asarray(label_test)
data_train = [data[i] for i in idxtrain]
data_train = np.asarray(data_train)
label_train = [label[i] for i in idxtrain]
label_train = np.asarray(label_train)

x = tf.placeholder(tf.float32, [None, 10000])
W = tf.Variable(tf.zeros([10000,3]))
y_ = tf.placeholder("float", [None,3])
sess = tf.InteractiveSession()

def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

x_image = tf.reshape(x, [-1,100,100,1])


W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


W_fc1 = weight_variable([25 * 25 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 25 * 25 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
W_fc2 = weight_variable([1024, 3])
b_fc2 = bias_variable([3])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())



def next_batch(num, data1, data2):

    idx = np.arange(0, len(data1))
    np.random.shuffle(idx)
    idx = idx[0:num]
    data_shuffle1 = [data1[i] for i in idx]
    data_shuffle1 = np.asarray(data_shuffle1)
    data_shuffle2 = [data2[i] for i in idx]
    data_shuffle2 = np.asarray(data_shuffle2)


    return [data_shuffle1,data_shuffle2]


p_x = [0 for i in range(10000)]
p_y = [0 for i in range(10000)]


with open("single_result.txt", "a") as log:
	for i in range(10000):

		dataset = next_batch(50, data_train, label_train)
		if i%1 == 0:
	
			train_accuracy = accuracy.eval(feed_dict={x:data_test, y_:label_test, keep_prob: 1.0})
			print("step %d, training accuracy %g"%(i, train_accuracy))
			p_x[i] = i
			p_y[i] = train_accuracy
			log.write(str(p_y[i]))
			log.write(", ")
		train_step.run(feed_dict={x:dataset[0], y_:dataset[1], keep_prob: 0.5})



