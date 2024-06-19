# Analyze
On Intel CPU system we have fastest inference with yolov8n model exported to OpenVINO format.

All analytics you can find [here](https://habr.com/ru/articles/822917/)

# Run server
```bash
cd server
python3 server.py
```

# Run client
```bash
pip3 install -r requirements.txt
python3 remote_run.py
```
