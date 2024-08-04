import requests

API_REQUEST = {
    "name": "foundry-api-key",
    "expiration": "10d",
    "role_descriptors": {
        "role-name": {
            "cluster": ["all"],
            "index": [{"names": ["*"], "privileges": ["all"]}],
        }
    },
}

url = "https://172.20.1.82:9200/_security/api_key"
post = requests.post(url, json=API_REQUEST, verify="http-ca.crt", auth=("elastic","rAyby7M7vJK750KUCzIZ"))
print(post.text)