### FastAPI를 활용해서 AI 서버를 만들 수 있음
# https://fastapi.tiangolo.com/tutorial/first-steps/

from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image, ImageDraw
import torch
from torchvision import transforms
import io
import requests
from ultralytics import YOLO

app = FastAPI()

# 기본 엔드포인트
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# YOLOv8 모델 로드
model = YOLO("yolov8n.pt")  # yolov8n.pt, yolov8s.pt, yolov8m.pt 등 원하는 모델 선택 가능

@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    try:
        # 업로드된 파일 읽기
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # 이미지 리사이즈
        image = image.resize((640, 640))  # YOLOv8 모델에 맞게 크기 조정

        # 객체 탐지 수행
        results = model.predict(image)

        # 탐지된 결과 추출
        detected_objects = []
        for result in results[0].boxes:
            detected_objects.append({
                "xmin": result.xyxy[0][0].item(),
                "ymin": result.xyxy[0][1].item(),
                "xmax": result.xyxy[0][2].item(),
                "ymax": result.xyxy[0][3].item(),
                "confidence": result.conf[0].item(),
                "class": int(result.cls[0].item()),
                "name": model.names[int(result.cls[0].item())]
            })

        return JSONResponse(content={"detected_objects": detected_objects})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/detect_and_draw/")
async def detect_objects_and_draw(file: UploadFile = File(...)):
    try:
        # 업로드된 파일 읽기
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # 이미지 리사이즈
        original_size = image.size
        image = image.resize((640, 640))  # YOLOv8 모델에 맞게 크기 조정

        # 객체 탐지 수행
        results = model.predict(image)

        # 박스 그리기
        draw = ImageDraw.Draw(image)
        for result in results[0].boxes:
            xmin = result.xyxy[0][0].item()
            ymin = result.xyxy[0][1].item()
            xmax = result.xyxy[0][2].item()
            ymax = result.xyxy[0][3].item()
            draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=2)
            label = f"{model.names[int(result.cls[0].item())]}: {result.conf[0].item():.2f}"
            draw.text((xmin, ymin), label, fill="red")

        # 이미지를 원래 크기로 리사이즈
        image = image.resize(original_size)

        # 이미지 반환
        byte_arr = io.BytesIO()
        image.save(byte_arr, format="JPEG")
        byte_arr.seek(0)
        return StreamingResponse(byte_arr, media_type="image/jpeg")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    

    # 이미지 테스트 curl
    # curl -X POST "http://127.0.0.1:8000/detect/" -F "file=@C:\Users\user\Downloads\ZN.35413463.1.jpg"
    # curl -X POST "http://127.0.0.1:8000/detect_and_draw/" -F "file=@C:\Users\user\Downloads\ZN.35413463.1.jpg" --output output.jpg

