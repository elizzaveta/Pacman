import csv
from os.path import exists

class StatisticsDQN:
    def __init__(self):
        self.filename = "statistics/dqn_train_process.csv"
        self.check_existence()


    def check_existence(self):
        if exists(self.filename): return

        f = open(self.filename, 'w', newline="")
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["GameNumb", "Score", "Time"])
        f.close()



    def add_statistics(self, game_numb, score, time):
        csv_file = open(self.filename, "a", newline="")
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow([str(game_numb), str(score), str(int(time))])
        csv_file.close()