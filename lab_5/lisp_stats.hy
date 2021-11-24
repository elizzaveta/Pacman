(import [pandas :as pd])
(import [numpy :as np])

(setv path "statistics/pacman_game_statistics.csv")
(setv data (pd.read_csv path))

(setv time (get data "Time"))
(print "Time mean:" (.mean time))

(setv score (get data "Score"))
(print "Score variance:" (.var score))
