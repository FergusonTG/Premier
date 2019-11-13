import requests

url = "https://www.footballwebpages.co.uk/league-table.json?" + \
    "comp=2&show=pos,pts&sort=normal"

response = requests.get(url)

print(response.text)
