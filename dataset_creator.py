from statistics import mean

import pandas
import csv
with open("ppg_dataset.csv", 'w', newline="\n") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(["points_scored", "ppg", "opponent_ppg", "win_perc",
                     "opponnent_win_perc", "last_10_win_perc", "opponent_last_10_win_perc"])

for year in range(2014, 2020):
    n = 0

    print(year)
    df = pandas.read_csv("game_data/games"+str(year)+".csv")
    teams = {}
    for i in df.index:
        try:
            visitor = df.at[i, "visitor"]
            visitor_score = df.at[i, "visitor_score"]
            home = df.at[i, "home"]
            home_score = df.at[i, "home_score"]
            if home not in teams.keys():
                home_perc = 1
                visitor_perc = 0
                if home_score-visitor_score < 0:
                    home_perc = 0
                    visitor_perc = 1
                teams[home] = {
                    "ppg": home_score,
                    "opponent_ppg": visitor_score,
                    "games_played": 1,
                    "win_total": home_perc,
                    "last_10": [home_perc]
                }
                teams[visitor] = {
                    "ppg": visitor_score,
                    "opponent_ppg": home_score,
                    "games_played": 1,
                    "win_total": visitor_perc,
                    "last_10": [visitor_perc]
                }
                continue
            home_win = 1
            visitor_win = 0
            if home_score - visitor_score < 0:
                visitor_win = 1
                home_win = 0
            home_win_perc = teams[home]['win_total'] / teams[home]['games_played']
            home_last_10_win_perc = mean(teams[home]['last_10'])
            visitor_win_perc = teams[visitor]['win_total'] / teams[visitor]['games_played']
            visitor_last_10_win_perc = mean(teams[visitor]['last_10'])


            home_row = [home_score, teams[home]['ppg'], teams[visitor]['opponent_ppg'],
                        home_win_perc, visitor_win_perc, home_last_10_win_perc, visitor_last_10_win_perc]
            print(home_row)
            teams[home]['ppg'] = (teams[home]['games_played'] * teams[home]['ppg'] + home_score) / (
                    teams[home]['games_played']+1)
            teams[home]['games_played'] += 1
            teams[home]['win_total'] += home_win
            if len(teams[home]['last_10']) == 10:
                teams[home]['last_10'].pop(0)
            teams[home]['last_10'].append(home_win)


            visitor_row = [visitor_score, teams[visitor]['ppg'], teams[home]['opponent_ppg'],
                           visitor_win_perc, home_win_perc, visitor_last_10_win_perc, home_last_10_win_perc]
            print(visitor_row)
            teams[visitor]['ppg'] = (teams[visitor]['games_played'] * teams[visitor]['ppg'] + visitor_score) / (
                        teams[visitor]['games_played'] + 1)
            teams[visitor]['opponent_ppg'] = (teams[visitor]['games_played'] * teams[visitor]['opponent_ppg'] + home_score) / (
                        teams[visitor]['games_played'] + 1)
            teams[visitor]['games_played'] += 1
            teams[visitor]['win_total'] += visitor_win
            if len(teams[visitor]['last_10']) == 10:
                teams[visitor]['last_10'].pop(0)
            teams[visitor]['last_10'].append(visitor_win)
            if n < 60:
                n+=1
                continue

            with open("ppg_dataset.csv", 'a', newline="\n") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow(home_row)
                writer.writerow(visitor_row)

        except KeyError:
            print("keyerror, skipping")