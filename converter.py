import csv

teams = {}

STREAK_CONST = 1

class Team:
    def __init__(self, name):
        self.name = name
        self.streak = 0
        self.winsStreak = 0
        self.lossesStreak = 0
        self.winsNoStreak = 0
        self.lossesNoStreak = 0


with open('game_data/games2018.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    skipFirst = 0
    for row in reader:
        if skipFirst == 0:
            skipFirst = 1
            continue
        visitor = row[0]
        visitor_score = row[1]
        home = row[2]
        home_score = row[3]
        if teams.get(visitor) == None:
            teams[visitor] = Team(visitor)
        if teams.get(home) == None:
            teams[home] = Team(home)

        if visitor_score > home_score:
            if teams[visitor].streak >= STREAK_CONST:
                teams[visitor].winsStreak += 1
            else:
                teams[visitor].winsNoStreak += 1

            if teams[home].streak >= STREAK_CONST:
                teams[home].lossesStreak += 1
            else:
                teams[home].lossesNoStreak += 1
            teams[home].streak = 0;
            teams[visitor].streak += 1
        else:
            if teams[home].streak >= 1:
                teams[home].winsStreak += 1
            else:
                teams[home].winsNoStreak += 1

            if teams[visitor].streak >= 1:
                teams[visitor].lossesStreak += 1
            else:
                teams[visitor].lossesNoStreak += 1
            teams[visitor].streak = 0
            teams[home].streak += 1
with open("streakOne2018.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                         quoting=csv.QUOTE_MINIMAL)
    i = 0
    avgWinStreak = 0
    avgWinNoStreak = 0
    writer.writerow(["name", "streak win %", "no streak win %"])
    for team in teams.values():
        if(team.name == "0"):
            continue

        streakWinPercentage = round(team.winsStreak / (team.winsStreak+team.lossesStreak), 2)
        noStreakWinPercentage = round(team.winsNoStreak / (team.winsNoStreak + team.lossesNoStreak), 2)
        writer.writerow([team.name, streakWinPercentage, noStreakWinPercentage])
        avgWinStreak = ((avgWinStreak * i)+streakWinPercentage)/(i+1)
        avgWinNoStreak = ((avgWinNoStreak * i) + noStreakWinPercentage) / (i + 1)
        i+=1
    writer.writerow(["average", round(avgWinStreak, 2), round(avgWinNoStreak, 2)])


