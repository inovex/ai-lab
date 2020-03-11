from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Dropout, Dense, Dot, Lambda, \
    Reshape, concatenate, GlobalMaxPooling1D, BatchNormalization, \
    Activation, Conv1D
from tensorflow.keras.initializers import Constant
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import Regularizer

import numpy as np


class OrthogonalRegularizer(Regularizer):
    """
    Considering that input is flattened square matrix X, regularizer tries to ensure that matrix X
    is orthogonal, i.e. ||X*X^T - I|| = 0. L1 and L2 penalties can be applied to it
    """    
    def __init__(self, l1=0.0, l2=0.0):
        self.l1 = K.cast_to_floatx(l1)
        self.l2 = K.cast_to_floatx(l2)

    def __call__(self, x):
        size = int(np.sqrt(x.shape[1].value))
        assert size * size == x.shape[1].value
        x = K.reshape(x, (-1, size, size))
        xxt = K.batch_dot(x, x, axes=(2, 2))
        regularization = 0.0
        if self.l1:
            regularization += K.sum(self.l1 * K.abs(xxt - K.eye(size)))
        if self.l2:
            regularization += K.sum(self.l2 * K.square(xxt - K.eye(size)))

        return regularization
    
    def get_config(self):
        return {'l1': float(self.l1), 'l2': float(self.l2)}
    

    

def orthogonal(l1=0.0, l2=0.0):
    """
    Functional wrapper for OrthogonalRegularizer.
    :param l1: l1 penalty
    :param l2: l2 penalty
    :return: Orthogonal regularizer to append to a loss function
    """
    return OrthogonalRegularizer(l1, l2)


def transform_net(inputs, dense_bn, conv1d_bn, scope=None, regularize=False):
    """
    Generates an orthogonal transformation tensor for the input preprocessing
    :param inputs: tensor with input image (either BxNxK or BxNx1xK)
    :param scope: name of the grouping scope
    :param regularize: enforce orthogonality constraint
    :return: BxKxK tensor of the transformation
    """
    with K.name_scope(scope):

        input_shape = inputs.get_shape().as_list()
        k = input_shape[-1]

        net = conv1d_bn(inputs, num_filters=64, kernel_size=1, padding='valid',
                        use_bias=True, scope='tconv1')
        net = conv1d_bn(net, num_filters=128, kernel_size=1, padding='valid',
                        use_bias=True, scope='tconv2')
        net = conv1d_bn(net, num_filters=1024, kernel_size=1, padding='valid',
                        use_bias=True, scope='tconv3')

        net = GlobalMaxPooling1D(data_format='channels_last')(net)

        net = dense_bn(net, units=512, scope='tfc1', activation='relu')
        net = dense_bn(net, units=256, scope='tfc2', activation='relu')

        transform = Dense(units=k * k,
                          kernel_initializer='zeros', bias_initializer=Constant(np.eye(k).flatten()),
                          activity_regularizer=orthogonal(l2=0.001) if regularize else None)(net)

        transform = Reshape((k, k))(transform)

    return transform

