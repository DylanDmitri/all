import requests
from bs4 import BeautifulSoup
import time
import re


def go():

    print(time.time())

    r = requests.get('https://smash.gg/tournament/smash-summit-5/Voting')
    soup = BeautifulSoup(r.text, 'html5lib')

    divs = soup.findAll('div', {'class':"col-md-4 col-sm-6 col-xs-6 bottom-spacer summit-player-column summit-player-container"})

    for d in divs:
        name = None
        if 'ChuDat' in d.text:
            name = 'Chudat'
        elif 'aMSa' in d.text:
            name = 'aMSa'
        elif 'S2J' in d.text:
            name = 'S2J'
        elif 'Reeve' in d.text:
            name = 'Reeve'

        if name is not None:
            result = re.search('(\d+,\d+)</small>', str(d))

            print(name, end=': ')
            print(result.group(1))

while True:
    go()
    time.sleep(30)