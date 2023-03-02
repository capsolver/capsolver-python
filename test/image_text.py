import capsolver
from pathlib import Path
import os
import base64

img_path = os.path.join(Path(__file__).resolve().parent,"queue-it.jpg")

with open(img_path,'rb') as f:
    img = base64.b64encode(f.read()) .decode("utf8")
    solution = capsolver.solve({
        "type":"ImageToTextTask",
        "module":"queueit",
        "body":img
        })
    print(solution)

    solution = capsolver.solve({
        "type":"HCaptchaClassification",
        "queries":[img],
        "question":"Please click each image containing a truck"
    })
    print(solution)