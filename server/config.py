models = {
    "base": [
        ("yolov8n.pt", "12qTtp-hjls6N0UMLbkurzxHzuhpWxqWt", False),
        ("yolov8s.pt", "1ga8jan6BvP8Pbmphx9HHBvby96jQgjHS", False),
        ("yolov8m.pt", "1r0ph4mbFsiuuRDxJHAj3di9TFnzCXbUq", False),
        ("yolov8l.pt", "1f1SlM01l3EWvpH66fEqyrdsEe1F5PdFT", False),
        ("yolov8x.pt", "1stXAXeDSgaMFv8AkZwtiw5RXvInd74tQ", False),
    ],
    "openvino": [
        ("yolov8n_openvino_base_openvino_model", "1A0O8iK23T9x0yX5sEy-Hvd0j_ZAttCKb", True),
        ("yolov8n_openvino_half_openvino_model", "1B2FSJv5RV-fc0YsX10n6dBaJvC-eOCEq", True),
        ("yolov8n_openvino_int8_openvino_model", "18PyBs5ktB46nJCnv6PcEaHFZ_p4DRM9U", True),

        ("yolov8s_openvino_base_openvino_model", "1ejRBsLHUHOGK8sda_bXdJd_PPUDkDhpx", True),
        ("yolov8s_openvino_half_openvino_model", "14_dFDo4rnumxA7nzGXwS5tg1sSHL3Hq6", True),
        ("yolov8s_openvino_int8_openvino_model", "1P3R7Nu3M0bYz_8OiHuyopQ8TWLK4V6Sz", True),

        ("yolov8m_openvino_base_openvino_model", "1a4mqHICsVL48i7LXmosqS0bOLuITB6s9", True),
        ("yolov8m_openvino_half_openvino_model", "1sltYBHF1yVmw8QhO9ZIXrINxR3ekbu0z", True),
        ("yolov8m_openvino_int8_openvino_model", "1buMeXWTHHxVrT5o9VgYWE1zjPxtpbvVB", True),

        ("yolov8l_openvino_base_openvino_model", "1_NAjGu9S9_n4z2vw3S65zHFQvmx0ZEVc", True),
        ("yolov8l_openvino_half_openvino_model", "12sWjisIBAgotkb7VjUqwTNstK5wutptK", True),
        ("yolov8l_openvino_int8_openvino_model", "1-0TYWUYt6CCl99nMdqLNUH12QCqXFQ3T", True),

        ("yolov8x_openvino_base_openvino_model", "1auiTSisn2SAbws2C3yiC_fJf5Yb4Tv3b", True),
        ("yolov8x_openvino_half_openvino_model", "1xlaM7NQR2YcJEDaJt9bxVu-Q7qwEdvwQ", True),
        ("yolov8x_openvino_int8_openvino_model", "1Pju0ySDnFZ2AxySmoZTqQJT0wxQy2Iqs", True),
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
