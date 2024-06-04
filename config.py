BASE_MODELS = [
    ["yolov8n.pt"],
    ["yolov8s.pt"],
    ["yolov8m.pt"],
    ["yolov8l.pt"],
    ["yolov8x.pt"]
]

EXPORTED_MODELS_PATH = "./exported_models"

TEST_IMAGES = ["./assets/images/bus.jpg"]
DEVICES = ["cpu"]
CSV_HEADER = ['model', 'runtime', 'inference_time', 'fps', 'accurate_time', 'half', 'int8']

# What to test
TEST_BASE = 1
TEST_EXPORTED = 1

MODEL_FILTER = None #lambda x: "openvino" in x or "ncnn" in x
DELAY_BETWEEN_TESTS = 0.1