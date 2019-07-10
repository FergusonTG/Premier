# Here is a url for getting the current points and positions:
# https://www.footballwebpages.co.uk/league-table.json?comp=1&show=pos,pts&sort=normal

from collections import Counter
import urllib.request
import json

url = "https://www.footballwebpages.co.uk/league-table.json?" + \
    "comp=1&show=pos,pts&sort=normal"

with urllib.request.urlopen(url) as response:
    datatext = response.read()
    table = json.loads(datatext)['leagueTable']['team']

scores = [int(team["points"]) for team in table]
print(scores)


bucket = 5
cn = Counter([s // bucket for s in scores])
for pts in range(max(cn), min(cn)-1, -1):
    s = "*" * cn[pts]
    print("{:2d} - {:2d}\t{}".format(
        pts * bucket,
        pts * bucket + bucket - 1,
        s)
    )
