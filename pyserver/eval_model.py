from __future__ import print_function
import tensorflow as tf
import cv2
import numpy as np
import os, random

model_loc = 'model/16_5000_model.ckpt'

def eval(t_x,model_fn=model_loc):   # ,data_dir=data_dir
    tf.reset_default_graph()
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(model_fn+'.meta')
        if os.path.isfile(model_fn+'.meta'):
            saver.restore(sess,model_fn)
        else:
            print("No model to load")
            return None
        return sess.run('out_:0',feed_dict={'X:0':t_x}) # ,'Y:0':t_y
#print(eval(get_test()[0]))
