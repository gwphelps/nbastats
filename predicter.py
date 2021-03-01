import csv


HOME_FACTOR = 1.17

teams = {}
games = []
correctPredictions = 0
total = 0


class Team:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0

def predict(visitor, home):
    if teams.get(visitor) == None:
        teams[visitor] = Team(visitor)
        if teams.get(home) == None:
            teams[home] = Team(home)
        return home
    if teams.get(home) == None:
        teams[home] = Team(home)
        if teams.get(visitor) == None:
            teams[visitor] = Team(visitor)
        return home
    #print(str(teams[visitor].wins) + ':' + str(teams[visitor].losses) + " " + str(teams[home].wins) + ':' +str(teams[home].losses))

    visitor_win_percentage = teams[visitor].wins / (teams[visitor].losses+teams[visitor].wins)

    home_win_percentage = teams[home].wins / (teams[home].losses+teams[home].wins) * HOME_FACTOR

    if visitor_win_percentage > home_win_percentage:
        return visitor
    elif visitor_win_percentage <= home_win_percentage:
        return home


date = 2014
for i in range(date, date+5):
    print(i)
    with open('games'+str(i)+'.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        skipFirst = 0
        for row in reader:

            if skipFirst == 0:
                skipFirst = 1
                continue
            visitor = row[0]
            visitor_score = int(row[1])
            home = row[2]
            home_score = int(row[3])

            prediction = predict(visitor, home)
            winner = ""
            if visitor_score > home_score:
                winner = visitor
                teams[visitor].wins += 1
                teams[home].losses += 1
            else:
                winner = home
                teams[home].wins += 1
                teams[visitor].losses += 1
            if(winner == prediction):
                correctPredictions += 1
            total += 1
        print(correctPredictions/total)


