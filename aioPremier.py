# Here is a url for getting the current points and positions:
# https://www.footballwebpages.co.uk/league-table.json?comp=1&show=pos,pts&sort=normal

from collections import Counter
import asyncio
import aiohttp


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
    scores = [int(team['points']) for team in teams]

    return scores


def histogram(scores, bucket_size=5):
    '''convert a set of scores into a histogram'''
    cn = Counter([s // bucket_size for s in scores])

    print(cn)

    for pts in range(max(cn), min(cn)-1, -1):
        s = "*" * cn[pts]
        print("{:2d} - {:2d}\t{}".format(
            pts * bucket_size,
            pts * bucket_size + bucket_size - 1,
            s)
        )


async def main():
    url = "https://www.footballwebpages.co.uk/league-table.json"
    params = {'comp': 1, 'show': 'pos,pts', 'sort': 'normal'}
    scores = await fetch(url, params)
    histogram(scores)


if __name__ == '__main__':
    asyncio.run(main())
