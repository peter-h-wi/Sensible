import requests
import json
resp = requests.get("https://v2.jokeapi.dev/joke/Programming?type=single")
x = json.loads(resp.text)
print(x["joke"])
