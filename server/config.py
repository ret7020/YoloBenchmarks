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
    "ncnn": [
        ("yolov8n_ncnn_base_ncnn_model", "1YyN8M2rzjitslnKuntwsHhati5AU8J-1", True),
        ("yolov8n_ncnn_half_ncnn_model", "1lgft4bl9Vr3IL8NBKzlDNJAbGxob988E", True),
        ("yolov8n_ncnn_int8_ncnn_model", "1d1mvQbEviFHgKapM-oYOdNCfB0jwnKmE", True),

        ("yolov8s_ncnn_base_ncnn_model", "1Rfn7EgyWs0NzZZNUslqhSD99YcQNXMd9", True),
        ("yolov8s_ncnn_half_ncnn_model", "1j_DYrJBxQVzpOnWIKlcfyw3avW4ROyEH", True),
        ("yolov8s_ncnn_int8_ncnn_model", "1TSErD_XiTCnyskfCjv5GQ4i48h_dEE0S", True),

        ("yolov8m_ncnn_base_ncnn_model", "1_gfbc7VfvewdGc_g6j_jfeUv7DxjYfqV", True),
        ("yolov8m_ncnn_half_ncnn_model", "1Ngi0-82kHXay-tk2UIOdG6YoSMY3OdgC", True),
        ("yolov8m_ncnn_int8_ncnn_model", "1kmNKd1G-PEHR-bZ02LBLkTViMVmKoFRJ", True),

        ("yolov8l_ncnn_base_ncnn_model", "1pfr6HX76nVfNkomJ2yPH4Vxq4sgUxQ_p", True),
        ("yolov8l_ncnn_half_ncnn_model", "165pgm_qde_RBwqsY8maXhaRxR0kIN9mt", True),
        ("yolov8l_ncnn_int8_ncnn_model", "13cYGHWes9aVjbsLJuTSgT5m7B-Hzx-j5", True),

        ("yolov8x_ncnn_base_ncnn_model", "1NWjD7oaJkj3UDB3c0xc-uTCbaFL5jSFQ", True),
        ("yolov8x_ncnn_half_ncnn_model", "1SmL1w9AKg1wqlAoozXWZY8VOXKUYU7fU", True),
        ("yolov8x_ncnn_int8_ncnn_model", "11wpqqNqBFLrB_LAtHe-4q7D85o7OYsQn", True),
    ],
    "tflite": [ # Only int8 and base
        ("yolov8n_tflite_base.tflite", "12JklYm_syFXUD8RIuz7NamnOGHJuY2f4", False),
        ("yolov8n_tflite_int8.tflite", "13R6fMsrgSUWCmhPwnzjG_cONELm_ILHA", False),

        ("yolov8s_tflite_base.tflite", "1fDjnWg7J_JDMFT4GGkukHajKrl-1hIvT", False),
        ("yolov8s_tflite_int8.tflite", "1Sg0N3aS2ScF-IFjmnwqHN2G07bCuzW9F", False),

        ("yolov8m_tflite_base.tflite", "1yibB58XegQKpM1eTu8eRTPBbdgrv5MnS", False),
        ("yolov8m_tflite_int8.tflite", "1X3XvhsF1E1eJMSMxQcbCtGKE1EBYxDWh", False),

        ("yolov8l_tflite_base.tflite", "1P_7XCBydGRPFFrHne4sO8pl1BDxAZfK9", False),
        ("yolov8l_tflite_int8.tflite", "1brBlAZeYaAzkKFN2RdCc3B19y1vRmwPk", False),

        ("yolov8x_tflite_base.tflite", "19OjHwP8EbCLS28gDMg-R3oRHpha-9vBH", False),
        ("yolov8x_tflite_int8.tflite", "1pbX9LutPxddef_0Km2CcF3xC4Ocqz6K6", False),
        
    ],
    "onnx": [],
    "tensorRT": ["CUDAyolov8n.pt"]
}

videos = [("adekvat.mp4", "1fr2j7hWL9HBTnLSJSpXD_LoZWeJg567v")]

abs_path = ""
video_path = "files/videos"
model_path = "files/models"
python_files_path = "files/py"
analytics_path = "files/analytics"

CSV_HEADER = ['model', 'runtime', 'inference_time_1', 'fps', 'inference_time', 'device', 'half', 'int8', 'map50', 'map75', 'warmup_max_inf_time', 'warmup_min_inf_time', 'inference_time_max', 'inference_time_min']
