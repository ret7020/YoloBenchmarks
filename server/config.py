models = {
    "base": ["yolov8n.pt"],
    "openvine": ["openyolov8n.pt"],
    "tensotRT": ["CUDAyolov8n.pt"]
}

videos = ["adekvat.mp4"]

abs_path = ""
video_path = "files/videos"
model_path = "files/models"
python_files_path = "files/py"
analytics_path = "files/analytics"

CSV_HEADER = ['model', 'runtime', 'inference_time_1', 'fps', 'inference_time', 'device', 'half', 'int8', 'map50', 'map75', 'warmup_max_inf_time', 'warmup_min_inf_time', 'inference_time_max', 'inference_time_min']
