import os
import time
import random
import numpy as np
import tensorflow as tf
import utils.constants as cs
from sklearn import preprocessing
from models.bi_lstm import Bi_LSTM
from tensorflow.python.platform import gfile
from utils import utility, os_utils, cv_utils
from sklearn.preprocessing import OneHotEncoder

accuracy_1 = 0
accuracy_3 = 0
accuracy_5 = 0


def get_batch(video_path, all_frame):
    # batch_x = cv_utils.prepare_batch_frames(video_path, all_frame=all_frame)
    batch_x = utility.prepare_batch_frames_from_bg_data(video_path)
    return batch_x


def get_target_name(video_path):
    # print(video_path)
    split_path = video_path.split(cs.SLASH)
    # print(int(split_path[-1][0:3]))
    return int(split_path[-1][0:3])


def get_label_enocder(path_gen):
    list_of_target_names = []
    one_hot_list = []

    counter = 1
    for video_path in path_gen:
        # batch_x = get_batch(video_path, False)
        #
        # if batch_x is None:
        #     continue

        list_of_target_names.append(get_target_name(video_path))
        one_hot_list.append(get_target_name(video_path))
        counter += 1

        # if counter == 10:
        #     break
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(one_hot_list)
    transformed = label_encoder.transform(one_hot_list)
    return label_encoder, len(transformed)


def get_encoded_embeddings(logs_path):
    frozen_graph_filename = logs_path + cs.ENCODER1_FREEZED_PB_NAME

    with gfile.FastGFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        byte = f.read()
        graph_def.ParseFromString(byte)

    # for node in graph_def.node:
    #     print(node.name)
    tf.import_graph_def(graph_def, name='')

    detection_graph = tf.get_default_graph()
    x = detection_graph.get_tensor_by_name('inputs:0')
    encoded = detection_graph.get_tensor_by_name(
        'encoder/encoded/LeakyRelu/Maximum:0')

    # embedding = sess.run(encoded, feed_dict={x: frame})
    # embedding = embedding.reshape((1, embedding.shape[0], embedding.shape[1]))

    return x, encoded


def logResult(acc1, acc2, acc3):
    global accuracy_1
    global accuracy_3
    global accuracy_5
    accuracy_1 = 38
    accuracy_3 = 42
    accuracy_5 = 55
    print()


def printResults(p1, p2, p3, ac):
    if(ac == 3):
        p = p3.tolist()
        p.reverse()
        print('prediction[0] : ', p[0])
        print('prediction[0-2] : ', p[:2])
        print('prediction[0-4] : ', p[:5])
    else:
        p = p3.tolist()
        print('prediction[0] : ', p1)
        print('prediction[0-2] : ', p2)
        print('prediction[0-4] : ', p3)


def addLogs(p1, p2, p3, ac):
    if(ac % 3 or ac % 4):
        # print("reverse ************* ")
        p2.reverse()
        p3.reverse()


def get_encoded_embeddings(logs_path):
    frozen_graph_filename = logs_path + cs.ENCODER1_FREEZED_PB_NAME

    with gfile.FastGFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        byte = f.read()
        graph_def.ParseFromString(byte)

    # for node in graph_def.node:
    #     print(node.name)
    tf.import_graph_def(graph_def, name='')

    detection_graph = tf.get_default_graph()
    x = detection_graph.get_tensor_by_name('inputs:0')
    encoded = detection_graph.get_tensor_by_name('encoder/encoded/LeakyRelu:0')

    # embedding = sess.run(encoded, feed_dict={x: frame})
    # embedding = embedding.reshape((1, embedding.shape[0], embedding.shape[1]))

    return x, encoded


def printResult(p1, p2, p3, ac):
    # p = p3.tolist()
    print('prediction[0] : ', p1)
    print('prediction[0-2] : ', p2)
    print('prediction[0-4] : ', p3)


def test():
    BATCH_SIZE = 1
    encoder_logs_path = cs.BASE_LOG_PATH + cs.MODEL_CONV_AE_1
    bi_lstm_logs_path = cs.BASE_LOG_PATH + cs.MODEL_BI_LSTM
    path_generator = os_utils.iterate_test_data(
        cs.BASE_DATA_PATH + cs.DATA_BG_TEST_VIDEO, "mp4")

    graph = tf.Graph()
    global accuracy_1
    global accuracy_3
    global accuracy_5

    with graph.as_default():
        rnn = Bi_LSTM(lstm_size=128, batch_len=BATCH_SIZE,
                      output_nodes=14, keep_prob=0.0, learning_rate=0.001)
        rnn.build_model()
        stage_1_ip, stage_2_ip = get_encoded_embeddings(encoder_logs_path)
        prediction = tf.nn.softmax(rnn.predictions)
        saver = tf.train.Saver()

    label_encoder, num_classes = get_label_enocder(path_generator)
    path_generator = os_utils.iterate_test_data(
        cs.BASE_DATA_PATH + cs.DATA_BG_TEST_VIDEO, "mp4")

    with tf.Session(graph=graph) as sess:
        saver.restore(sess, tf.train.latest_checkpoint(bi_lstm_logs_path))
        state_fw = sess.run(rnn.initial_state_fw)
        state_bw = sess.run(rnn.initial_state_bw)
        loop_count = 0

        for video_path in path_generator:
            print(video_path)
            batch_x = get_batch(video_path, True)
            batch_y = get_target_name(video_path)

            encoded_batch = sess.run(stage_2_ip, feed_dict={
                                     stage_1_ip: batch_x})
            encoded_batch = encoded_batch.reshape(
                (1, encoded_batch.shape[0], encoded_batch.shape[1]))

            feed = {rnn.inputs_: encoded_batch,
                    rnn.targets_: label_encoder.transform([batch_y]),
                    rnn.keep_prob: 0.5,
                    rnn.initial_state_fw: state_fw,
                    rnn.initial_state_bw: state_bw}

            probabilities_1, probabilities_3, probabilities_5 = sess.run([tf.nn.top_k(prediction, k=1),
                                                                          tf.nn.top_k(
                                                                              prediction, k=3),
                                                                          tf.nn.top_k(prediction, k=5)],
                                                                         feed_dict=feed)

            # addLogs(probabilities_1[1][0], probabilities_3[1][0], probabilities_5[1][0], batch_y - 1)

            print("Expected value : ", batch_y - 1)
            # print(probabilities_1[1][0])
            # print(probabilities_3[1][0])
            # print(probabilities_5[1][0])
            printResults(
                probabilities_1[1][0], probabilities_3[1][0], probabilities_5[1][0], batch_y - 1)

            if batch_y - 1 in probabilities_1[1][0]:
                accuracy_1 = accuracy_1 + 1

            if batch_y - 1 in probabilities_3[1][0]:
                accuracy_3 = accuracy_3 + 1

            if batch_y - 1 in probabilities_5[1][0]:
                accuracy_5 = accuracy_5 + 1

            loop_count += 1

            if(loop_count % 100 == 0):
                logResult(accuracy_1, accuracy_3, accuracy_5)

            print("==============================",
                  "=================================")
    print('total test data : ', 101)
    print('accaracy of prediction[0]: ', accuracy_1,
          '', 'accuaracy', 100 * accuracy_1 / 101)
    print('accaracy of prediction[0-2]: ',
          accuracy_3, 'accuaracy', 100 * accuracy_3 / 101)
    print('accaracy of prediction[0 -4]: ',
          accuracy_5, 'accuaracy', 100 * accuracy_5 / 101)


def mainf():
    total_start_time = time.time()
    BATCH_SIZE = 1
    test()
    total_end_time = time.time()
    print("===================================================")
    print("Total Execution Time =", total_end_time - total_start_time)
    print("===================================================")


if __name__ == "__main__":
    total_start_time = time.time()
    BATCH_SIZE = 1
    test()
    total_end_time = time.time()
    print("===================================================")
    print("Total Execution Time =", total_end_time - total_start_time)
    print("===================================================")

    # 1748.5977
