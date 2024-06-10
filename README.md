# Analyze
On Intel CPU system we have fastest inference with yolov8n model exported to OpenVINO format.

# TODO

- [x] Add warmup (5 frames) before benchmarked
- [ ] Analyze OpenVINO int8 model
- [ ] Check custom trained model
- [ ] Write min/max warmup
- [ ] Write min/max inference
- [ ] Write after inference model to csv file
- [ ] Write model size
- [ ] Select test source from config
- [ ] Set task to model to prevent warnings
- [ ] Other tasks (seg, classify) perf check
- [ ] How to use instruction
- [ ] Lite requirements (Yolo can install runtimes on fly)
- [ ] Selectable inference device
- [x] Write 1/0 instead True/False to csv report in int8/half sections
- [x] Remove ./exported_models/ from csv name
- [x] Disable yolo visualize