import time
import json
import uuid
import hmac
import base64
import hashlib
import requests

base_url = "https://ip:port"
appKey = "****"
appSecret = "****"


def hik_request(secret, key, path, body):
    x_ca_nonce = str(uuid.uuid4())
    x_ca_timestamp = str(int(round(time.time()) * 1000))
    sign_str = (
        "POST\n*/*\napplication/json"
        + "\nx-ca-key:"
        + key
        + "\nx-ca-nonce:"
        + x_ca_nonce
        + "\nx-ca-timestamp:"
        + x_ca_timestamp
        + "\n"
        + path
    )
    temp = hmac.new(secret.encode(), sign_str.encode(), digestmod=hashlib.sha256)
    signature = base64.b64encode(temp.digest()).decode()
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "x-ca-key": appKey,
        "x-ca-signature-headers": "x-ca-key,x-ca-nonce,x-ca-timestamp",
        "x-ca-signature": signature,
        "x-ca-timestamp": x_ca_timestamp,
        "x-ca-nonce": x_ca_nonce,
    }
    response = requests.post(
        base_url + path, data=json.dumps(body), headers=headers, verify=False
    )
    return response


body = {
    "cameraIndexCode": "****",
    "protocol": "hls",
}
data = hik_request(
    appSecret, appKey, "/artemis/api/video/v2/cameras/previewURLs", body
)
print(data)
print(data.json())
