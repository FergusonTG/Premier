# Here is a url for getting the current points and positions:
# https://www.footballwebpages.co.uk/league-table.json?comp=1&show=pos,pts&sort=normal

from pprint import pprint
from collections import Counter
import asyncio
import aiohttp


DEBUG = False
COMPETITION = 2   # 1 = Premier, 2 = Championship
BUCKET_SIZE = 3
TEAM_NAME = "Cardiff City"


async def fetch(url, params):
    '''Get json object from the url'''

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                print(response.status)
                raise aiohttp.ClientError(
                    'Page request failed, code {}'.format(response.status)
                )

            data = await response.json()

    teams = data['leagueTable']['team']

    # Debug only: pretty print the teams list
    if DEBUG:
        pprint(teams)

    # strip out just the scores for all teams
    scores = [int(team['points']) for team in teams]

    # locate how many points our team scored
    team_score = [int(team['points']) for team in teams
                  if team['name'] == TEAM_NAME][0]

    return scores, team_score


def histogram(scores, team_score, bucket_size=BUCKET_SIZE):
    '''convert a set of scores into a histogram'''
    cn = Counter([s // bucket_size for s in scores])
    ts = team_score // bucket_size

    # DEBUG print list of scores
    if DEBUG:
        print(cn)

    for pts in range(max(cn), min(cn)-1, -1):
        stars = "*" * cn[pts]
        print("{:s} {:2d} - {:2d}\t{}".format(
            "#" if pts == ts else " ",
            pts * bucket_size,
            pts * bucket_size + bucket_size - 1,
            stars,
        ))


async def main():
    url = "https://www.footballwebpages.co.uk/league-table.json"
    params = {'comp': COMPETITION, 'show': 'pos,pts', 'sort': 'normal'}
    scores, team_score = await fetch(url, params)
    histogram(scores, team_score)


if __name__ == '__main__':
    asyncio.run(main())
