import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2

# YOLOv8 모델 로드
@st.cache_resource
def load_model():
    model = YOLO('yolov8n.pt')
    return model

model = load_model()

# 사이드바 메뉴 설정
menu = st.sidebar.selectbox("Menu", ["Home", "Description"])

# "Home" 메뉴
if menu == "Home":
    st.title("YOLOv8 Object Detection")
    st.write("Upload an image to perform object detection using YOLOv8.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("")

        # Convert the image to numpy array
        image_np = np.array(image)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # YOLOv8 inference
        results = model(image_np)
        
        # Render the results
        annotated_frame = results[0].plot()  # Use plot() method for visualization
        annotated_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        st.image(annotated_image, caption='Annotated Image', use_column_width=True)

# "Description" 메뉴
elif menu == "Description":
    st.title("Description")
    st.write("""
        This application demonstrates the use of YOLOv8 for object detection. You can upload an image and see the detected objects highlighted in the image.
        
        ### How it works:
        1. **Model Loading**: The YOLOv8 model is loaded only once using Streamlit's caching mechanism.
        2. **Image Upload**: You can upload an image using the file uploader.
        3. **Object Detection**: The uploaded image is processed by the YOLOv8 model to detect objects.
        4. **Result Display**: The detected objects are highlighted and displayed on the image.
        
        **YOLOv8** (You Only Look Once version 8) is a state-of-the-art, real-time object detection system. It is pre-trained on a large dataset and can detect various objects in images.
    """)
