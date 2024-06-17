# This scripts converts base YOLOv8 models (from BASE_MODELS config.py file) 

from ultralytics import YOLO
from config import BASE_MODELS
import os
import shutil
from tqdm import tqdm
from termcolor import colored

if not os.path.exists("./exported_models"):
    os.mkdir("./exported_models")

# EXPORT_MODELS = [
#     {"format": "ncnn", "half": False, "int8": False, "optimize": False, "save_name": "ncnn_base_ncnn_model"},
#     {"format": "ncnn", "half": True, "int8": False, "optimize": False, "save_name": "ncnn_half_ncnn_model"},
#     {"format": "ncnn", "half": False, "int8": True, "optimize": False, "save_name": "ncnn_int8_ncnn_model"},
#     {"format": "onnx", "half": False, "int8": False, "optimize": True, "save_name": "onnx_base.onnx"},
#     {"format": "onnx", "half": False, "int8": True, "optimize": True, "save_name": "onnx_int8.onnx"},
#     {"format": "tflite", "half": False, "int8": False, "optimize": True, "save_name": "tflite_base.tflite"}
#     # half and int8
# ]

# EXPORT_MODELS = [
#     {"format": "openvino", "half": False, "int8": False, "optimize": True, "save_name": "openvino_base_openvino_model"},
#     {"format": "openvino", "half": True, "int8": False, "optimize": True, "save_name": "openvino_half_openvino_model"}
# ]

# EXPORT_MODELS = [
#    {"format": "openvino", "half": False, "int8": True, "optimize": True, "save_name": "openvino_int8_openvino_model"}
# ]
    
EXPORT_MODELS = [
    {"format": "openvino", "half": False, "int8": False, "optimize": True, "save_name": "cube_openvino_base_openvino_model"},
    {"format": "openvino", "half": True, "int8": False, "optimize": True, "save_name": "cube_openvino_half_openvino_model"},
    {"format": "openvino", "half": False, "int8": True, "optimize": True, "save_name": "cube_openvino_int8_openvino_model"},

    {"format": "ncnn", "half": False, "int8": False, "optimize": False, "save_name": "cube_ncnn_base_ncnn_model"},
    {"format": "ncnn", "half": True, "int8": False, "optimize": False, "save_name": "cube_ncnn_half_ncnn_model"},
    {"format": "ncnn", "half": False, "int8": True, "optimize": False, "save_name": "cube_ncnn_int8_ncnn_model"},

    {"format": "onnx", "half": False, "int8": False, "optimize": True, "save_name": "cube_onnx_base.onnx"},
    {"format": "onnx", "half": False, "int8": True, "optimize": True, "save_name": "cube_onnx_int8.onnx"},

    {"format": "tflite", "half": False, "int8": False, "optimize": True, "save_name": "cube_tflite_base.tflite"},
    {"format": "tflite", "half": False, "int8": True, "optimize": True, "save_name": "cube_tflite_base.tflite"}
]

EXPORT_MODELS = [
    {"format": "onnx", "half": False, "int8": False, "optimize": True, "save_name": "onnxnonsimp_base.onnx"},
    {"format": "onnx", "half": False, "int8": True, "optimize": True, "save_name": "onnxnonsimp_int8.onnx"},
]

# BASE_MODELS = ["base.pt"]
LOAD_PATH = 0
for model_name in tqdm(BASE_MODELS):
    
    model_name_full = model_name
    model_base_name = model_name[0].replace(".pt", "")
    if not LOAD_PATH:
        model_name = model_name[0]
    else:
        model_base_name = model_name_full.replace(".pt", "")
        print(model_name)

    for model_config in EXPORT_MODELS:
        print(colored(str(model_config), "green"))
        src2 = None
        dst2 = None
        if not LOAD_PATH:
            model = YOLO(model_name)
        else:
            model = YOLO(model_name_full)
        model.export(format=model_config["format"], half=model_config["half"], int8=model_config["int8"], simplify=False,
                optimize=model_config["optimize"], verbose=False)
        if model_config["format"] in ["ncnn"]:  # For ncnn
            src = f"./{model_base_name}_{model_config['format']}_model"
        elif model_config["format"] == "tflite":  # For tflite
            src = f"./{model_base_name}_saved_model/{model_base_name}_float32.tflite"
            src2 = f"./{model_base_name}_saved_model/{model_base_name}_float16.tflite"
            dst2 = f"./exported_models/{model_base_name}_tflite_int8.tflite"
        elif model_config["format"] == "openvino" and model_config["int8"]:
            src = f"./{model_base_name}_int8_{model_config['format']}_model"
        elif model_config["format"] == "openvino":  # For generic openvino model
            src = f"./{model_base_name}_{model_config['format']}_model"
        else:  # For onnx
            src = f"./{model_base_name}.{model_config['format']}"
        dst = f"./exported_models/{model_base_name}_{model_config['save_name']}"
        shutil.move(src, dst)
        if src2:
            shutil.move(src2, dst2)
