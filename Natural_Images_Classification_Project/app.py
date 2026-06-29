import tensorflow as tf
import numpy as np
import streamlit as st
import pandas as pd
import time
from PIL import Image
from tensorflow.keras.applications.vgg16 import preprocess_input

st.set_page_config(
    page_title='Natural Image Classifier',
    page_icon='📷',
    layout='centered',
    initial_sidebar_state='expanded'
)

CLASS_NAMES = [
    'airplane',    
    'car',         
    'cat',          
    'dog',         
    'flower',      
    'fruit',        
    'motorbike',    
    'person'        
]

@st.cache_resource()
def load_model():
    try:
        interpreter = tf.lite.Interpreter(model_path='natural_images.tflite')
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        st.error(f"TFLite Model Error: {e}")
        return None
    
model = load_model()

st.sidebar.title("📌 Navigation")
st.sidebar.divider()
st.sidebar.header('⚙️ System Configuration')

if model is not None:
    st.sidebar.success('🟢 Model Runtime: Online')
else:
    st.sidebar.error('🔴 Model Runtime: Offline')

st.sidebar.markdown("""
### About This App
This neural network parses raw RGB pixels to classify everyday subjects across 8 targeted categories using an optimized VGG TFLite engine execution pipeline.
""")

st.title('📷 Image Classification App')
st.markdown("##### Upload any clear image below to test the trained model's real-time computer vision inference engine.")
st.divider()

def preprocessing_image(image):
    image = image.convert('RGB')
    image = image.resize((224, 224))
    image = np.array(image, dtype=np.float32)          
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0) 
    return image

uploaded_file = st.file_uploader('Select an Image File...', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption='📷 Uploaded Context Image', width=300)
    
    with col2:
        st.subheader("Action Control")
        st.write("Click below to invoke the forward execution graph pass on the input matrix tensor.")
        predict_btn = st.button('🚀 Predict Class Label', type='primary', use_container_width=True)
    
    if predict_btn:
        if model is None:
            st.error("Execution Aborted: The TFLite runtime instance could not be safely instantiated.")
        else:
            with st.status('⚙️ Computing Tensor Graph Inference...', expanded=True) as status:
                start_time = time.time()
                
                preprocess = preprocessing_image(image)
                
                input_details = model.get_input_details()
                output_details = model.get_output_details()
                
                model.set_tensor(input_details[0]['index'], preprocess)
                model.invoke()
                
                prediction = model.get_tensor(output_details[0]['index'])[0]
                
                if np.min(prediction) < 0 or np.max(prediction) > 1.0:
                    exp_preds = np.exp(prediction - np.max(prediction))
                    prediction = exp_preds / exp_preds.sum()
                
                predict_index = np.argmax(prediction)
                predicted_class = CLASS_NAMES[predict_index]
                confidence = float(prediction[predict_index])
                
                latency = (time.time() - start_time) * 1000
                time.sleep(0.4)
                status.update(label="Inference Sequence Completed!", state="complete", expanded=False)
                
            st.balloons()
            
            st.success(f"### Prediction: **{predicted_class.upper()}**")
            st.info(f"💡 **Confidence Level:** {confidence:.2%}")
            st.metric(label="⚡ Inference Execution Latency", value=f"{latency:.2f} ms")
            
            st.markdown("#### 📊 Metric Category Probabilities Distribution:")
            chart_df = pd.DataFrame({
                'Probability': [float(p) for p in prediction]
            }, index=[c.capitalize() for c in CLASS_NAMES])
            st.bar_chart(chart_df)
