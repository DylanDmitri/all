import requests
import time
import pickle
import bs4 as soup
import fake_useragent
import dota2api

ua = fake_useragent.UserAgent()
recent_games_url = 'https://www.dotabuff.com/matches?lobby_type=ranked_matchmaking&skill_bracket=very_high_skill'

def recent():
    r = requests.get(recent_games_url, headers={'User-Agent': ua.random})
    text = r.text

    game_ids = []
    target = 'href="/matches/'
    offset = len(target)

    while True:
        l = text.find(target)
        if l < 0:
            break

        id = text[l+offset: l+offset+10]
        game_ids.append(id)
        text = text[l+offset:]

    return [e for i, e in enumerate(game_ids) if i%2]

url = 'http://api.opendota.com/api/matches/{}'.format

def info(match_id):
    return requests.get(url(match_id)).json()

def save(match_id):
    print('attemping match', match_id, end='')
    r = info(match_id)

    if 'players' in r and 'purchase_time' in r['players'][0]:

        try:
            open('match_results/all/'+str(match_id), 'r')
        except FileNotFoundError:
            print('; match already saved')
        else:
            f = open('match_results/all/' + str(match_id),'wb')
            pickle.dump(r, f)
            f.close()
            print('; match saved')

    else:
        print('; no details')





for id in recent():
    start = time.time()

    if True:
        save(id)

    while time.time() - start < 2:
        time.sleep(0.1)
