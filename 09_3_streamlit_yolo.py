import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image

# 사이드바 메뉴 설정
menu = st.sidebar.selectbox("Menu", ["Image Inference", "Description"])

# "Image Inference" 메뉴
if menu == "Image Inference":
    # Streamlit 앱 제목 설정
    st.title("YOLOv8 Image Inference")

    # 이미지 업로드
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 이미지를 PIL 형식으로 열기
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # YOLOv8 모델 불러오기
        model = YOLO('yolov8n.pt')  # 'yolov8n.pt'는 사전 학습된 YOLOv8 모델 가중치 파일입니다

        # 이미지를 numpy 배열로 변환
        image_np = np.array(image)

        # 모델을 이용한 추론
        results = model(image_np)

        # 추론 결과를 이미지에 그리기
        annotated_frame = results[0].plot()  # results.plot() 대신 results[0].plot() 사용

        # 결과 이미지 표시
        st.image(annotated_frame, caption='Model Inference Result', use_column_width=True)

# "Description" 메뉴
elif menu == "Description":
    st.title("Description")
    st.write("""
        This application demonstrates the use of the YOLOv8 model for image inference.
        - **Image Inference**: Upload an image to perform object detection using the YOLOv8 model.
        - **Description**: This section provides information about the application and its functionality.
        
        The YOLO (You Only Look Once) model is a state-of-the-art, real-time object detection system.
        It is widely used in various applications such as video surveillance, autonomous driving, and more.
    """)
