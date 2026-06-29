import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input

# Create Custom object for preprocess_input
custom_objects = {'preprocess_input' : preprocess_input}

# Load The Model 
model = tf.keras.models.load_model('natural_images_classification.h5',custom_objects = custom_objects)

# Convert to tflite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
with open('natural_images.tflite','wb') as f:
    f.write(tflite_model)

print("Model Converted Is Done!")