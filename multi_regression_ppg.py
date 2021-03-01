import pandas
from sklearn import linear_model
import csv
import matplotlib.pyplot as plt

def writeEquationToCSV(linear_mod):
    with open("nba_equation.csv", 'w', newline="\n") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(['ppg', "opponent_ppg", "win_perc", "opponent_win_perc",
                         "last_10_win_perc", "opponent_last_10_win_perc", 'intercept'])
        writer.writerow(([linear_mod.coef_[0], linear_mod.coef_[1],
                          linear_mod.coef_[2], linear_mod.coef_[3],
                          linear_mod.coef_[4], linear_mod.coef_[5],
                          linear_mod.intercept_]))

df = pandas.read_csv('ppg_dataset.csv')

X = df[['opponent_ppg']]#, "opponent_ppg", "win_perc","opponnent_win_perc","last_10_win_perc","opponent_last_10_win_perc"]]
y = df['points_scored']

linear_mod = linear_model.LinearRegression()
linear_mod.fit(X, y)

plt.scatter(X,y,color='yellow') #plotting the initial datapoints
plt.plot(X,linear_mod.predict(X),color='blue',linewidth=3) #plotting the line made by linear regression
plt.show()
#writeEquationToCSV(linear_mod)

