from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from playsound import playsound
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import threading

url = 'https://www.espn.com/nfl/game/_/gameId/401131041'
favHome = False
if len(sys.argv) == 2:
    favHome = True if (sys.argv[1].lower() == 'h') else False
diff = 6

if favHome:
    print('Home')
else:
    print('Away')

def playTD():
    playsound('td.mp3')

def playTDThread():
    t1 = threading.Thread(target=playTD)
    t1.setDaemon(True)
    t1.start()

def printScore(awayScore, homeScore):
    print('\r' + str(awayScore) + ' - ' + str(homeScore), end=' ', flush = True)

'''
# test
i = 1
while i < 10:
    playTDThread()
    print(i)
    time.sleep(0.05)
    i += 1
# end test
'''

print('Loading Score...', end = '', flush = True)
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver",options = options)
driver.get(url)
print('Done')

startBefore = False 

while True:
    html = driver.page_source
    bs = BeautifulSoup(html,'lxml')
    scores = bs.find_all('div',{'class': 'score'})
    if scores[0].get_text() == '':
        i = 60
        startBefore = True
        while i >= 0:
            print('\rThe game hasn\'t start yet, will try again after', i, 's ', end = '', flush = True)
            time.sleep(1)
            i -= 1
    else:
        if startBefore:
            print('\r                                                             ')
        else: 
            print('')
        break


awayScore = (int)(scores[0].get_text())
homeScore = (int)(scores[1].get_text())
printScore(awayScore, homeScore)



while True:
    html = driver.page_source
    bs = BeautifulSoup(html,'lxml')
    scores = bs.find_all('div',{'class': 'score'})
    if (int)(scores[0].get_text()) != awayScore:
        if (int)(scores[0].get_text()) - awayScore >= diff:
            #time.sleep(10)
            print('Away TD!!')
            if not favHome:
                playTDThread()
        else:
            print('Away scored!!')
    if (int)(scores[1].get_text()) != homeScore:
        if (int)(scores[1].get_text()) - homeScore >= diff:
            #time.sleep(10)
            print('Home TD!!')
            if favHome:
                playTDThread()
        else:
            print('Home scored!!')
    awayScore = (int)(scores[0].get_text())
    homeScore = (int)(scores[1].get_text())
    printScore(awayScore, homeScore)
    time.sleep(2)

    if 'final' in bs.find('span', {'class': 'game-time'}).get_text().lower():
        print('\nGame Ends')
        break

