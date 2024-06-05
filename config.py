BASE_MODELS = [
    ["yolov8n.pt"],
    ["yolov8s.pt"],
    ["yolov8m.pt"],
    ["yolov8l.pt"],
    ["yolov8x.pt"]
]

EXPORTED_MODELS_PATH = "./exported_models"

TEST_IMAGES = ["./assets/images/bus.jpg", "./assets/images/cars.jpg"]
DEVICES = ["cpu"]
CSV_HEADER = ['model', 'runtime', 'inference_time', 'fps', 'accurate_time', 'device', 'half', 'int8', 'mAP50', 'mAP75']
VALIDATE_CONFIG = "coco8.yaml"

# What to test
TEST_BASE = 1
TEST_EXPORTED = 0

MODEL_FILTER = None #lambda x: "openvino" in x or "ncnn" in x
DELAY_BETWEEN_TESTS = 0.1