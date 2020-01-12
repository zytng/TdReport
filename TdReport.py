from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from playsound import playsound
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

url = 'https://www.espn.com/nfl/game/_/gameId/401131041'
favHome = False
if len(sys.argv) == 2:
    favHome = True if (sys.argv[1].lower() == 'h') else False
diff = 6

if favHome:
    print('Home')
else:
    print('Away')

'''
# test
playsound('td.mp3')
print('test finished')
# end test
'''

def printScore(awayScore, homeScore):
    print('\r' + str(awayScore) + ' - ' + str(homeScore), end=' ', flush = True)


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
        if (not favHome) and (int)(scores[0].get_text()) - awayScore >= diff:
            #time.sleep(10)
            print('Away TD!!')
            playsound('td.mp3')
        else:
            print('Away scored!!')
        '''
        awayScore = (int)(scores[0].get_text())
        homeScore = (int)(scores[1].get_text())
        print(' ' + str(awayScore) + ' - ' + str(homeScore), end='\n')
        '''
    if (int)(scores[1].get_text()) != homeScore:
        if favHome and (int)(scores[1].get_text()) - homeScore >= diff:
            #time.sleep(10)
            print('Home TD!!')
            playsound('td.mp3')
        else:
            print('Home scored!!')
        '''
        awayScore = (int)(scores[0].get_text())
        homeScore = (int)(scores[1].get_text())
        print(' ' + str(awayScore) + ' - ' + str(homeScore), end='\n')
        '''
    awayScore = (int)(scores[0].get_text())
    homeScore = (int)(scores[1].get_text())
    printScore(awayScore, homeScore)
    time.sleep(2)

    if 'final' in bs.find('span', {'class': 'game-time'}).get_text().lower():
        print('\nGame Ends')
        break



'''
#time new
while True:
    html = driver.page_source
    bs = BeautifulSoup(html,'lxml')
    print('   ' + bs.find('span', class_='status-detail').get_text(), end = '\r')
'''







'''
html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
scores = bs.find_all('div',{'class': 'score'})
awayScore = (int)(scores[0].get_text())
homeScore = (int)(scores[1].get_text())
print(str(awayScore) + ' - ' + str(homeScore))

'''
'''
#time
while True:
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'html.parser')
    print('   ' + bs.find('span', class_='status-detail').get_text(), end = '\r')
'''
'''

while True:
    #print(str(awayScore) + ' - ' + str(homeScore))
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'html.parser')
    scores = bs.find_all('div',{'class': 'score'})

    if awayScore - (int)(scores[0].get_text()) >= 6:
        if not favHome:
            playsound('td.mp3')
        print('Away scored!!')
        awayScore = (int)(scores[0].get_text())
        print(str(awayScore) + ' - ' + str(homeScore))
    if homeScore - (int)(scores[1].get_text()) >= 6:
        if favHome:
            playsound('td.mp3')
        print('Home scored!!')
        homeScore = (int)(scores[1].get_text())
        print(str(awayScore) + ' - ' + str(homeScore))
        
    awayScore = (int)(scores[0].get_text())
    homeScore = (int)(scores[1].get_text())
    #time.sleep(2)
'''