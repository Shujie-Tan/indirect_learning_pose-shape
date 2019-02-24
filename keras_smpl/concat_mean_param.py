import tensorflow as tf
import numpy as np
import deepdish as dd

from keras import backend as K


def concat_mean_param(img_features):
    mean_path = './neutral_smpl_mean_params.h5'
    mean_vals = dd.io.load(mean_path)

    mean_pose = mean_vals['pose']
    # Ignore the global rotation.
    mean_pose[:3] = 0.
    mean_shape = mean_vals['shape']

    # Set initial smpl parameters
    mean = np.zeros((1, 86))
    mean[0, 4:] = np.expand_dims(np.hstack((mean_pose, mean_shape)), axis=0)

    # Set initial camera parameters - dependent on output image size!
    mean[0, 0] = 32.0
    mean[0, 1] = 32.0
    mean[0, 2] = 32.0
    mean[0, 3] = 40.0

    mean = tf.constant(mean, dtype='float32')
    mean = tf.tile(mean, [K.shape(img_features)[0], 1])

    state = tf.concat([img_features, mean], axis=1)
    return [state, mean]

# concat_mean_param(None)