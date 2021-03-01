from statistics import mean

import pandas

equation_df = pandas.read_csv('nba_equation.csv')

ppg_c = equation_df['ppg'][0]
o_ppg_c = equation_df['opponent_ppg'][0]
win_perc_c = equation_df['win_perc'][0]
o_win_perc_c = equation_df['opponent_win_perc'][0]
last_10_win_perc_c = equation_df['last_10_win_perc'][0]
o_last_10_win_perc_c = equation_df['opponent_last_10_win_perc'][0]
intercept = equation_df['intercept'][0]

winTotal = 0
lossTotal = 0
nTotal = 0
errorTotal = 0
for year in range(2014, 2020):
    winYear = 0
    lossYear = 0
    nYear = 0
    errorYear = 0
    print(year)
    df = pandas.read_csv("game_data/games" + str(year) + ".csv")
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
                if home_score - visitor_score < 0:
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

            home_prediction = round(ppg_c * teams[home]['ppg']
                                    + o_ppg_c * teams[visitor]['opponent_ppg']
                                    + win_perc_c * home_win_perc
                                    + o_win_perc_c * visitor_win_perc
                                    + last_10_win_perc_c * home_last_10_win_perc
                                    + o_last_10_win_perc_c * visitor_last_10_win_perc
                                    + intercept)
            visitor_prediction = round(ppg_c * teams[visitor]['ppg']
                                    + o_ppg_c * teams[home]['opponent_ppg']
                                    + win_perc_c * visitor_win_perc
                                    + o_win_perc_c * home_win_perc
                                    + last_10_win_perc_c * visitor_last_10_win_perc
                                    + o_last_10_win_perc_c * home_last_10_win_perc
                                    + intercept)
            spread_prediction = home_prediction - visitor_prediction

            actual_spread = home_score - visitor_score
            errorYear = (nYear * errorYear + abs(actual_spread - spread_prediction)) / (nYear+1)
            nYear += 1
            #print(str(spread_prediction) + " : "+str(actual_spread))
            if spread_prediction > 0:
                if actual_spread > 0:
                    winYear += 1
                else:
                    lossYear += 1
            elif spread_prediction < 0:
                if actual_spread < 0:
                    winYear += 1
                else:
                    lossYear += 1
            #else:
                #print("0, dont know how to account for that lol")








            teams[home]['ppg'] = (teams[home]['games_played'] * teams[home]['ppg'] + home_score) / (
                    teams[home]['games_played'] + 1)
            teams[home]['opponent_ppg'] = (teams[home]['games_played'] * teams[home][
                'opponent_ppg'] + visitor_score) / (teams[home]['games_played'] + 1)
            teams[home]['games_played'] += 1
            teams[home]['win_total'] += home_win
            if len(teams[home]['last_10']) == 1:
                teams[home]['last_10'].pop(0)
            teams[home]['last_10'].append(home_win)


            teams[visitor]['ppg'] = (teams[visitor]['games_played'] * teams[visitor]['ppg'] + visitor_score) / (
                    teams[visitor]['games_played'] + 1)
            teams[visitor]['opponent_ppg'] = (teams[visitor]['games_played'] * teams[visitor][
                'opponent_ppg'] + home_score) / (teams[visitor]['games_played'] + 1)
            teams[visitor]['games_played'] += 1
            teams[visitor]['win_total'] += visitor_win
            if len(teams[visitor]['last_10']) == 1:
                teams[visitor]['last_10'].pop(0)
            teams[visitor]['last_10'].append(visitor_win)
        except KeyError:
            print("keyerror continue...")
    print(year)
    print(str(winYear) + " wins")
    print(str(lossYear) + " losses")
    print(str(round(winYear/(winYear+lossYear)*100, 2)) + "%")
    print("spread was +-"+str(errorYear))
    winTotal += winYear
    lossTotal+= lossYear
    errorTotal = (nTotal * errorTotal + errorYear) / (nTotal + 1)
    nTotal += 1
print("total")
print(str(winTotal) + " wins")
print(str(lossTotal) + " losses")
print(str(round(winTotal/(winTotal+lossTotal)*100, 2)) + "%")
print("spread was +-"+str(errorTotal))
