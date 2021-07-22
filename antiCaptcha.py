from PIL import Image
from io import BytesIO
import base64
import requests
import time
import logging

def parse_captcha(image_path, token):
    # Load image into memory
    buffer = BytesIO()
    image = Image.open(image_path)
    image.save(buffer, format="PNG")
    # Use base64 to encode image buffer
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    # Anti-captcha API structure
    data = {
        "task": {
            "type": "ImageToTextTask",
            "body": img_str,
            "phrase":False,
            "case": False,
            "numeric": 2,
            "math": 0,
            "minLength": 4,
            "maxLength": 4
        }
    }
    data["clientKey"] = token

    logging.info("Sending requst to anti-captcha")
    # Create a ImageToTextTask and retrieve taskId from response
    r = requests.post("https://api.anti-captcha.com/createTask", json=data)
    r.raise_for_status()
    task_id = r.json()['taskId']

    logging.info("Polling task status...")
    # Polling for task finish.
    ret = ""
    while True:
        data = {
            'taskId': task_id
        }
        data["clientKey"] = token
        r = requests.post("https://api.anti-captcha.com/getTaskResult", json=data)
        r.raise_for_status()
        if r.json()['status'] == 'ready':
            ret = r.json()['solution']['text']
            break
        else:
            logging.info("Task not ready yet, wait 5 seconds")
            time.sleep(5)
    return ret