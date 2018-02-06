"""Honestbee Data Engineering team interview test"""

import hug
import json
import requests
from datetime import datetime, timedelta

INTERVALS = {
    'week': 7,
	'month': 30,
	'year': 365
}

def opendota(path, query=None):
    url = 'https://api.opendota.com/api/' + '/'.join(map(str,path))
    if query is not None:
        url += '?' + '&'.join([k+'='+str(v) for k,v in query.items()])
    res = requests.get(url)
    print(url)
    return json.loads(res.content.decode('utf-8'))

def resolve(player):
    if player.isdigit():
        return player
    else:
        data = opendota( ('search'), {'q': player, 'similarity': 1} )
        ## TODO: catch when there are no players returned
        return data[0]['account_id']

HEROES = None
def heroes():
    global HEROES
    if HEROES is not None:
        return HEROES
    data = opendota( ('heroes',) )
    HEROES = { str(hero['id']): hero['localized_name'] for hero in data }
    print('preloaded heroes')
    # print(HEROES)
    return HEROES

## Question 1
@hug.get('/leaderboard')
def leaderboard(player_ids: hug.types.multiple, time_frame: hug.types.text = 'week'):
    board = []
    ## handle if personaname is given instead of account_id
    players = [resolve(player_id) for player_id in player_ids]
    days = INTERVALS[time_frame]
    # now = datetime.now()
    for player in players:
        data = opendota( ('players', player, 'wl'), {'date': days} )
        wins = data['win']
        board.append({'account_id': player, 'wins': wins, 'win_rate': wins/days})
    return sorted(board, key=lambda x: -x['win_rate'])

## Question 2
@hug.get('/compare')
def compare(player_A: hug.types.text, player_B: hug.types.text):
    A = get_stats(player_A)
    B = get_stats(player_B)
    result = {}
    for A_stat, B_stat in zip(A, B):
        if A_stat[1] > B_stat[1]:
            result[A_stat[0]] = player_A
        else:
            result[A_stat[0]] = player_B
    return result

def get_stats(player):
    player = resolve(player)
    data = opendota( ('players', player, 'totals') )
    ## want kda, gpm, xpm [3:6]
    return map(lambda stat: (stat['field'], stat['sum']/stat['n'] if stat['n'] > 0 else 0), data)

## Question 3
@hug.get('/suggest')
def suggest(player: hug.types.text):
    player = resolve(player)
    data = opendota( ('players', player, 'heroes') )
    best_hero = max(data, key=lambda h: h['win']/h['games'] if h['games'] > 0 else 0)
    return heroes()[best_hero['hero_id']]
