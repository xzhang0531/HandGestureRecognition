import tensorflow as tf
import numpy as np
import tflearn
from tflearn.data_utils import shuffle, to_categorical

data1 = np.loadtxt('resizedData_a.txt',delimiter=', ')
data1 = data1.reshape(100,10000)
data2 = np.loadtxt('resizedData_b.txt',delimiter=', ')
data2 = data2.reshape(100,10000)
data3 = np.loadtxt('resizedData_c.txt',delimiter=', ')
data3 = data3.reshape(100,10000)
data4 = np.loadtxt('resizedData_d.txt',delimiter=', ')
data4 = data4.reshape(100,10000)
data5 = np.loadtxt('resizedData_e.txt',delimiter=', ')
data5 = data5.reshape(100,10000)
data6 = np.loadtxt('resizedData_f.txt',delimiter=', ')
data6 = data6.reshape(100,10000)
data7 = np.loadtxt('resizedData_g.txt',delimiter=', ')
data7 = data7.reshape(100,10000)
data8 = np.loadtxt('resizedData_h.txt',delimiter=', ')
data8 = data8.reshape(100,10000)
data9 = np.loadtxt('resizedData_i.txt',delimiter=', ')
data9 = data9.reshape(100,10000)
data10 = np.loadtxt('resizedData_k.txt',delimiter=', ')
data10 = data10.reshape(100,10000)
data11 = np.loadtxt('resizedData_l.txt',delimiter=', ')
data11 = data11.reshape(100,10000)
data12 = np.loadtxt('resizedData_m.txt',delimiter=', ')
data12 = data12.reshape(100,10000)
data13 = np.loadtxt('resizedData_n.txt',delimiter=', ')
data13 = data13.reshape(100,10000)
data14 = np.loadtxt('resizedData_o.txt',delimiter=', ')
data14 = data14.reshape(100,10000)
data15 = np.loadtxt('resizedData_p.txt',delimiter=', ')
data15 = data15.reshape(100,10000)
data16 = np.loadtxt('resizedData_q.txt',delimiter=', ')
data16 = data16.reshape(100,10000)
data17 = np.loadtxt('resizedData_r.txt',delimiter=', ')
data17 = data17.reshape(100,10000)
data18 = np.loadtxt('resizedData_s.txt',delimiter=', ')
data18 = data18.reshape(100,10000)
data19 = np.loadtxt('resizedData_t.txt',delimiter=', ')
data19 = data19.reshape(100,10000)
data20 = np.loadtxt('resizedData_u.txt',delimiter=', ')
data20 = data20.reshape(100,10000)
data21 = np.loadtxt('resizedData_v.txt',delimiter=', ')
data21 = data21.reshape(100,10000)
data22 = np.loadtxt('resizedData_w.txt',delimiter=', ')
data22 = data22.reshape(100,10000)
data23 = np.loadtxt('resizedData_x.txt',delimiter=', ')
data23 = data23.reshape(100,10000)
data24 = np.loadtxt('resizedData_y.txt',delimiter=', ')
data24 = data24.reshape(100,10000)
data = np.concatenate((data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18, data19, data20, data21, data22, data23, data24))


label1 = []
label2 = []
label3 = []
label4 = []
label5 = []
label6 = []
label7 = []
label8 = []
label9 = []
label10 = []
label11 = []
label12 = []
label13 = []
label14 = []
label15 = []
label16 = []
label17 = []
label18 = []
label19 = []
label20 = []
label21 = []
label22 = []
label23 = []
label24 = []
for i in range(100):
	label1.append(0)
	label2.append(1)
	label3.append(2)
	label4.append(3)
	label5.append(4)
	label6.append(5)
	label7.append(6)
	label8.append(7)
	label9.append(8)
	label10.append(9)
	label11.append(10)
	label12.append(11)
	label13.append(12)
	label14.append(13)
	label15.append(14)
	label16.append(15)
	label17.append(16)
	label18.append(17)
	label19.append(18)
	label20.append(19)
	label21.append(20)
	label22.append(21)
	label23.append(22)
	label24.append(23)

label1 = np.array(label1)
label2 = np.array(label2)
label3 = np.array(label3)
label4 = np.array(label4)
label5 = np.array(label5)
label6 = np.array(label6)
label7 = np.array(label7)
label8 = np.array(label8)
label9 = np.array(label9)
label10 = np.array(label10)
label11 = np.array(label11)
label12 = np.array(label12)
label13 = np.array(label13)
label14 = np.array(label14)
label15 = np.array(label15)
label16 = np.array(label16)
label17 = np.array(label17)
label18 = np.array(label18)
label19 = np.array(label19)
label20 = np.array(label20)
label21 = np.array(label21)
label22 = np.array(label22)
label23 = np.array(label23)
label24 = np.array(label24)
label = np.concatenate((label1, label2, label3, label4, label5, label6, label7, label8, label9, label10, label11, label12, label13, label14, label15, label16, label17, label18, label19, label20, label21, label22, label23, label24))
label = to_categorical(label,24)


idx = np.arange(0, len(data))
np.random.shuffle(idx)
idxtest = idx[0:500]
idxtrain = idx[500:2400]
data_test = [data[i] for i in idxtest]
data_test = np.asarray(data_test)
label_test = [label[i] for i in idxtest]
label_test = np.asarray(label_test)
data_train = [data[i] for i in idxtrain]
data_train = np.asarray(data_train)
label_train = [label[i] for i in idxtrain]
label_train = np.asarray(label_train)

x = tf.placeholder(tf.float32, [None, 10000])
W = tf.Variable(tf.zeros([10000,24]))
y_ = tf.placeholder("float", [None,24])
sess = tf.InteractiveSession()
saver = tf.train.Saver()


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
W_fc2 = weight_variable([1024, 24])
b_fc2 = bias_variable([24])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()


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
	for i in range(2000):

		dataset = next_batch(50, data_train, label_train)
		if i%1 == 0:
	
			train_accuracy = accuracy.eval(feed_dict={x:data_test, y_:label_test, keep_prob: 1.0})
			print("step %d, training accuracy %g"%(i, train_accuracy))
			p_x[i] = i
			p_y[i] = train_accuracy
			log.write(str(p_y[i]))
			log.write(", ")
		train_step.run(feed_dict={x:dataset[0], y_:dataset[1], keep_prob: 0.5})



save_path = saver.save(sess, "D:/HandGestureRecognition/Model/model.ckpt")
print("Model saved in path: %s" % save_path)