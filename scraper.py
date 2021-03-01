# This is a sample Python script.
import requests
from bs4 import BeautifulSoup
import csv
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
YEAR = str(2014)
OUTPUT_FILE = "game_data/games2014.csv"

class Game:
    def __init__(self, team1, score1, team2, score2):
        self.team1 = team1
        self.score1 = score1
        self.team2 = team2
        self.score2 = score2


months = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]
gameArr = []

for month in months:
    url = "https://www.basketball-reference.com/leagues/NBA_"+YEAR+"_games-"+month+".html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    gameList = soup.find(id='schedule').find_all('tr')
    first = 0
    for game in gameList:
        if first == 0:
            first = 1
            continue
        
        i = 0
        team1 = 0
        score1 = ""
        team2 = 0
        score2 = ""
        for column in game.find_all('td'):
            #print(column.text)
            if i == 1:
                team1 = column.text
            if i == 2:
                score1 = column.text
            if i == 3:
                team2 = column.text
            if i == 4:
                score2 = column.text
            if i == 5:
                boxScoreUrl = "https://www.basketball-reference.com" + column.find("a", href=True)['href']
                boxScorePage = requests.get(url)
                boxScoreSoup = BeautifulSoup(boxScorePage.content, 'html.parser')

                
            i += 1
        gameObj = Game(team1, score1, team2, score2)
        gameArr.append(gameObj)
with open(OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                         quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["visitor", "visitor_score", "home", "home_score"])
    for game in gameArr:
        writer.writerow([game.team1, game.score1, game.team2, game.score2])








