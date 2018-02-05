"""A simple example of a hug API call with versioning"""
import hug
import json
import dota2api
import requests
from datetime import datetime, timedelta

#api = dota2api.Initialise()
#match = api.get_match_details(match_id=1000193456)

def api(path, query=None):
    url = 'https://api.opendota.com/api/' + '/'.join(map(str,path))
    if query is not None:
        url += '?' + '&'.join([k+'='+str(v) for k,v in query.items()])
    res = requests.get(url)
    return json.loads(res.content.decode('utf-8'))

#@hug.get('/match')
#def match(id):
#    return api.get_match_details(match_id=id)

@hug.get('/leaderboard')
def comparison(player_ids: hug.types.multiple, time_frame: hug.types.text):
    board = []
    ## handle if personaname is given instead of account_id
    for player_id in player_ids:
        if player_id.isdigit():
            board.append({'account_id': player_id})
        else:
            data = api( ('search'), {'q': player_id, 'similarity': 1} )
            board.append({'account_id': data[0]['account_id']})
    now = datetime.now()
    if time_frame == 'week':
        days = 7
    if time_frame == 'month':
        days = 30
    if time_frame == 'year':
        days = 365
    for player in board:
        data = api( ('players', player['account_id'], 'wl'), {'date': days} )
        wins = data['win']
        player['wins'] = wins
        player['win_rate'] = float(wins)/days
    #subset = filter(lambda x: datetime.fromtimestamp(x['start_time']) >= now - timedelta(days=days), res['matches'])
    #return subset
    # return map(lambda x: x['match_id'], res['matches'])
    return board

@hug.get('/unversioned')
def hello():
    return 'Hello world!'
