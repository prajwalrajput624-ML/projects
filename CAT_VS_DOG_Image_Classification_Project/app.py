import numpy as np
import tensorflow as tf
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'CAT Vs DOG Image Classification App',
    page_icon = '🐾',
    layout = 'centered'
)

@st.cache_resource()
def load_model():
    try:
        custom_objects = {
            'preprocess_input': tf.keras.applications.resnet50.preprocess_input
        }
        return tf.keras.models.load_model(
            'CAT_Vs_DOG_Image_Classification_Model.keras', 
            custom_objects=custom_objects
        )
    except Exception as e:
        st.error(f"Model Path Error: {e}")
        return None

model = load_model()

def Image_preprocessing(image):
    image = image.convert('RGB')
    image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis = 0)
    return image

st.sidebar.title('🧭 Navigation')
st.sidebar.divider()
st.sidebar.header('⚙️ System Info')

if model is not None:
    st.sidebar.success('Model Online')
else:
    st.sidebar.error('Model Offline')

st.title('🐾 CAT Vs DOG Image Classification')
st.divider()
st.write('Please Upload Only RGB Image')

uploaded_file = st.file_uploader('Choose an Image...', type = ['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = 'Uploaded Image', width = 350)
    
    if st.button('Predict', type = 'primary'):
        if model is not None:
            with st.status('Analyzing Image...', expanded = True) as status:
                preprocess = Image_preprocessing(image)
                prediction = model.predict(preprocess)
                prob = float(prediction)
                
                if prob > 0.5:
                    label = "Dog"
                    confidence = prob * 100
                else:
                    label = "Cat"
                    confidence = (1 - prob) * 100
                    
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
            st.success(f"Prediction: {label}")
            st.balloons()
            st.progress(int(confidence))
            st.write(f"Confidence: {confidence:.2f}%")
