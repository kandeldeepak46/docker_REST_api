import requests

from loguru import logger

host = "http://localhost:9999"

r = requests.get(f"{host}/train")
logger.info(r.text)

payload = [
    {"Age": 85, "Sex": "male", "Embarked": "S"},
    {"Age": 24, "Sex": "female", "Embarked": "C"},
    {"Age": 3, "Sex": "male", "Embarked": "C"},
    {"Age": 21, "Sex": "male", "Embarked": "S"},
]

r = requests.post(f"{host}/predict", json=payload)
logger.info(r.text)


#if you dont want to remove the model.comment the following code
r = requests.get(f"{host}/wipe")
logger.info(r.text)

"""
from urllib.parse import urlparse
import http.client as ht
def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = ht.HTTPConnection(url.netloc)
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl
getStatus(ourl="http://127.0.0.1:5000/train")
"""
