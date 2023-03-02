# Capsolver
Capsolver official python library

## Supported CAPTCHA types:
- HCaptcha
- FunCaptcha
- Geetest
- ReCaptchaV2
- ReCaptchav3
- MtCaptcha
- Datadom
- Cloudflare
- Kasada
- Akamai BMP


## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip3 install --upgrade capsolver
```

Install from source with:

```sh
python setup.py install
```

## Usage

```bash
export CAPSOLVER_API_KEY='...'
```

Or set `capsolver.api_key` to its value:

```python
from pathlib import Path
import os
import base64
import capsolver

# tokenTask
print("api host",capsolver.api_base)
print("api key",capsolver.api_key)
# capsolver.api_key = "..."
solution = capsolver.solve({
        "type":"ReCaptchaV2TaskProxyLess",
        "websiteKey":"6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        "websiteURL":"https://www.google.com/recaptcha/api2/demo",
    })

print(solution)

# RecognitionTask
img_path = os.path.join(Path(__file__).resolve().parent,"queue-it.jpg")
with open(img_path,'rb') as f:
    solution = capsolver.solve({
        "type":"ImageToTextTask",
        "module":"queueit",
        "body":base64.b64encode(f.read()).decode("utf8")
    })
    print(solution)

# get current balance
balance = capsolver.balance()
# print the current balance
print(balance)
```


