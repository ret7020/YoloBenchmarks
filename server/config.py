models = {
    "base": [
        ("yolov8n.pt", "12qTtp-hjls6N0UMLbkurzxHzuhpWxqWt", False),
        ("yolov8s.pt", "1ga8jan6BvP8Pbmphx9HHBvby96jQgjHS", False),
        ("yolov8m.pt", "1r0ph4mbFsiuuRDxJHAj3di9TFnzCXbUq", False),
        ("yolov8l.pt", "1f1SlM01l3EWvpH66fEqyrdsEe1F5PdFT", False),
        ("yolov8x.pt", "1stXAXeDSgaMFv8AkZwtiw5RXvInd74tQ", False),
    ],
    "openvino": [
        ("yolov8n_openvino_base_openvino_model", "1_NAjGu9S9_n4z2vw3S65zHFQvmx0ZEVc", True),
        ("yolov8n_openvino_half_openvino_model", "1B2FSJv5RV-fc0YsX10n6dBaJvC-eOCEq", True),
        ("yolov8n_openvino_int8_openvino_model", "18PyBs5ktB46nJCnv6PcEaHFZ_p4DRM9U", True)
    ],
    "tensorRT": ["CUDAyolov8n.pt"]
}

videos = [("adekvat.mp4", "1fr2j7hWL9HBTnLSJSpXD_LoZWeJg567v")]

abs_path = ""
video_path = "files/videos"
model_path = "files/models"
python_files_path = "files/py"
analytics_path = "files/analytics"

CSV_HEADER = ['model', 'runtime', 'inference_time_1', 'fps', 'inference_time', 'device', 'half', 'int8', 'map50', 'map75', 'warmup_max_inf_time', 'warmup_min_inf_time', 'inference_time_max', 'inference_time_min']
