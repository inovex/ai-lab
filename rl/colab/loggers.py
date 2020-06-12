import io

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from PIL import Image


def tf_summary_image(obs):
    height, width = obs.shape
    image = Image.fromarray(obs)
    output = io.BytesIO()
    image.save(output, format='PNG')
    image_string = output.getvalue()
    output.close()

    return tf.Summary.Image(height=height,
                            width=width,
                            colorspace=1,
                            encoded_image_string=image_string)


class TensorBoardLogger:
    def __init__(self, log_dir):
        self.writer = tf.summary.FileWriter(log_dir)

    def log_scalar(self, name, value, global_step):
        summary = tf.Summary(value=[tf.Summary.Value(tag=name, simple_value=value)])
        self.writer.add_summary(summary, global_step)

    def log_image(self, name, image, global_step):
        summary = tf.Summary(value=[tf.Summary.Value(tag=name, image=image)])
        self.writer.add_summary(summary, global_step)
