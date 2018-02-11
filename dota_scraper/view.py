import pickle
from dota_scraper.heroes import heroes


def view(match_id):
    r = pickle.load(open('match_results/all/'+str(match_id), 'rb'))
    print(r)

view(3070331101)



