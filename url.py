import requests

url = "https://www.footballwebpages.co.uk/league-table.json?" + \
    "comp=1&show=pos,pts&sort=normal"

response = requests.get(url)

print(response.text)
