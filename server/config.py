models = {
    "base": ["yolov8n.pt"],
    "openvine": ["openyolov8n.pt"],
    "tensotRT": ["CUDAyolov8n.pt"]
}

videos = ["vidos.mp4"]

abs_path = ""
video_path = "files/videos"
model_path = "files/models"
python_files_path = "files/py"
analytics_path = "files/analytics"

CSV_HEADER = ['model', 'runtime', 'inference_time', 'fps', 'accurate_time', 'device', 'half', 'int8', 'mAP50', 'mAP75']
