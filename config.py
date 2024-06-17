BASE_MODELS = [
    ["yolov8n.pt"],
    ["yolov8s.pt"],
    ["yolov8m.pt"],
    ["yolov8l.pt"],
    ["yolov8x.pt"]
]

EXPORTED_MODELS_PATH = "./exported_models"

TEST_IMAGES = ["./assets/images/bus.jpg", "./assets/images/cars.png"]
TEST_SOURCE = "images: " # if camera:source:cnt it will use camera (example, camera:0:10 -> cv2.VideoCapture(0); read 20 frames from camera)
DEVICES = ["cpu"]
CSV_HEADER = ['model', 'runtime', 'inference_time_1', 'fps', 'inference_time', 'device', 'half', 'int8', 'map50', 'map75', 'warmup_max_inf_time', 'warmup_min_inf_time']
VALIDATE_CONFIG = "coco8.yaml"
WARMUP_IMAGES = 5

# What to test
TEST_BASE = 1
TEST_EXPORTED = 0
DELAY_BETWEEN_TESTS = 0.1

# Only for exported models
MODEL_FILTER = lambda x: "openvino" in x


# TODO
TASK = "detect" # segment; classify
VALIDATE = 0