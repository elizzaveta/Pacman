import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from statistics import *

""" class for linear regression """
class LRegression:

    def __init__(self, file_path):
        self.dataset = pd.read_csv(file_path)
        self.regressor = LinearRegression()
        self.X_test = None
        self.y_test = None
        self.X_train = None
        self.y_train = None
        self.train_regressor()
        self.filename = 'statistics/pacman_game_statistics_predicted.csv'

    """ train regression model according to given data file """
    def train_regressor(self):
        X = self.dataset['Time'].values.reshape(-1, 1)
        y = self.dataset['Score'].values.reshape(-1, 1)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.9, random_state=0)
        self.regressor.fit(self.X_train, self.y_train)

    """ draw plot of actual values vs predicted values """
    def predicted_vs_test_plot(self):
        y_pred = self.regressor.predict(self.X_test)
        plt.scatter(self.X_test, self.y_test, color='gray')
        plt.plot(self.X_test, y_pred, color='red', linewidth=2)
        plt.show()

    """ display predicted values vs actual """
    def display_predicted_n_samples(self, n):
        if n>len(self.X_test): n = len(self.X_test)
        y_pred = self.regressor.predict(self.X_test[0:n])
        df = pd.DataFrame({'Actual': self.y_test[0:n].flatten(), 'Predicted': y_pred.flatten()})
        print("Actual vs Predicted values:")
        print(df)
        self.write_predicted_into_csv(y_pred, self.X_test[0:n])

    """ estimate absolute error """
    def display_error(self):
        y_pred = self.regressor.predict(self.X_test)
        print('Mean Absolute Error:', metrics.mean_absolute_error(self.y_test, y_pred))

    """ draw values plot """
    def show_dataset_plot(self):
        self.dataset.plot(x='Time', y='Score', style='o')
        plt.title('Time vs Score')
        plt.xlabel('Time')
        plt.ylabel('Score')
        plt.show()

    """ write predicted n values to file """
    def write_predicted_into_csv(self, predicted, time):
        csv_file = open(self.filename, "w", newline="")
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Game result", "Time", "Score", "Algorithm"])
        index = 0
        for score in predicted:
            result = 'Lose'
            if score > 96:
                result = 'Win'
            csv_writer.writerow([result, str(float(time[index])), str(int(score)), 'alpha-beta'])
            index+=1
        csv_file.close()


