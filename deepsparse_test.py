from deepsparse import Pipeline
import time
import cv2

model_path = "/tmp/yolov8n.onnx" # Base ONNX export


yolo_pipeline = Pipeline.create(task="yolov8", model_path=model_path)


cap = cv2.VideoCapture("./data/videos/adekvat.mp4")
for i in range(200):
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 640))
    start_time = time.time()
    pipeline_outputs = yolo_pipeline(images=[frame])
    print(1 / (time.time() - start_time))
    # for box in pipeline_outputs.boxes[0]:
    #     cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
    