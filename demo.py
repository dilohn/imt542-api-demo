import requests

# Your ngrok URL here
BASE = "YOUR_URL"

# GET / "Hello, World!"
print(requests.get(BASE + "/").text)

# GET /hello/name/<username>
print(requests.get(f"{BASE}/hello/name/Bob").text)

# GET /sbir/state/<state>
resp = requests.get(f"{BASE}/sbir/state/NY")
if resp.ok:
    print("NY award:", resp.text)
else:
    print("NY not found (status)", resp.status_code)

# POST /sbir/state
resp = requests.post(f"{BASE}/sbir/state", json={"state": "NY"})
print("POST response:", resp.json())
