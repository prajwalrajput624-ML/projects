import os
import numpy as np
import tensorflow as tf
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='CAT Vs DOG Image Classification App',
    page_icon='🐾',
    layout='centered'
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'cat_dog_model.tflite')

@st.cache_resource()
def load_model():
    try:
        interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        st.error(f"Model Load Error: {e}")
        return None

interpreter = load_model()

def Image_preprocessing(image):
    image = image.convert('RGB')
    image = image.resize((224, 224))
    image = np.array(image, dtype=np.float32)
    image = tf.keras.applications.resnet50.preprocess_input(image)
    return np.expand_dims(image, axis=0)

def predict(interpreter, image):
    input_details  = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])

st.sidebar.title('🧭 Navigation')
st.sidebar.divider()
st.sidebar.header('⚙️ System Info')

if interpreter is not None:
    st.sidebar.success('✅ Model Online')
else:
    st.sidebar.error('❌ Model Offline')

st.title('🐾 CAT Vs DOG Image Classification')
st.divider()
st.write('Please Upload Only RGB Image')

uploaded_file = st.file_uploader('Choose an Image...', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', width=350)

    if st.button('Predict', type='primary'):
        if interpreter is not None:
            with st.status('Analyzing Image...', expanded=True) as status:
                preprocessed = Image_preprocessing(image)
                prediction   = predict(interpreter, preprocessed)
                prob         = float(prediction[0][0])

                if prob > 0.5:
                    label      = "🐶 Dog"
                    confidence = prob * 100
                else:
                    label      = "🐱 Cat"
                    confidence = (1 - prob) * 100

                status.update(label="Analysis Complete!", state="complete", expanded=False)

            st.success(f"Prediction: {label}")
            st.balloons()
            st.progress(int(confidence))
            st.write(f"Confidence: {confidence:.2f}%")

        else:
            st.error("Model failed to load! Please check logs.")
