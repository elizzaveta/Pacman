import csv
from os.path import exists

class Statistics:
    def __init__(self):
        self.filename = "../statistics/pacman_game_statistics.csv"
        self.check_existence()


    def check_existence(self):
        if exists(self.filename): return

        f = open(self.filename, 'w', newline="")
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Game result", "Time", "Score", "Algorithm"])
        f.close()



    def add_statistics(self, if_win, time, score, algorithm):
        csv_file = open(self.filename, "a", newline="")
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        result = "Win"
        if if_win == 0: result = "Lose"
        csv_writer.writerow([result, str(time), str(score), str(algorithm)])
        csv_file.close()


