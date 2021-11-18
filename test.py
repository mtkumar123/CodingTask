import requests

response = requests.get("http://0.0.0.0:5000/info")
print(response.json())
input()
response = requests.post("http://0.0.0.0:5000/ping", data={"url": "https://www.google.com"})
print(response.json())
