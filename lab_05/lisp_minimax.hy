(defn move_left [agent]
    [(- (get agent 0) 1) (get agent 1)]
)
(defn move_right[agent]
    [(+ (get agent 0) 1)(get agent 1)]
)
(defn move_up[agent]
    [(get agent 0) (- (get agent 1) 1)]
)
(defn move_down[agent]
    [(get agent 0) (+ (get agent 1) 1)]
)

(defn heuristics [pacman ghost]
    (+ (abs (- (get pacman 0) (get ghost 0))) (abs (- (get pacman 1) (get ghost 1))))
)
(defn is_terminal [pacman ghost depth]
    (or (and (= (get pacman 0) (get ghost 0)) (= (get pacman 1) (get ghost 1))) (= depth 2))
)

(defn get_possible_moves[agent maze]
    (setv left (move_left agent))
    (setv right (move_right agent))
    (setv up (move_up agent))
    (setv down (move_down agent))
    (setv moves [])

    (if (=(get maze (get left 0) (get left 1)) 0) (moves.append left))
    (if (=(get maze (get right 0) (get right 1)) 0)(moves.append right))
    (if (=(get maze (get up 0) (get up 1)) 0) (moves.append up))
    (if (=(get maze (get down 0) (get down 1)) 0) (moves.append down))
    (return moves)
)



(defn minimax [maze pacman ghost depth]
    (maximize maze pacman ghost depth)
)

(defn maximize[maze pacman ghost depth]
    (if (is_terminal pacman ghost depth) (return (heuristics pacman ghost)))
    (setv move_cost [[0 0] -1])

    (setv moves (get_possible_moves pacman maze))

    (for [move moves]
        (setv cost (minimize maze move ghost (+ depth 1)))
        (if (> cost (get move_cost 1)) (setv move_cost [move cost]))
    )

    (return move_cost)
)

(defn minimize[maze pacman ghost depth]
    (if (is_terminal pacman ghost depth) (return (heuristics pacman ghost)))
    (setv move_cost [[0 0] 100])

    (setv moves (get_possible_moves ghost maze))

    (for [move moves]
        (setv cost (maximize maze pacman move (+ depth 1)))
        (if (< cost (get move_cost 1)) (setv move_cost [move cost]))
    )

     (return(get move_cost 1))
)




(setv maze [[1 1 1 1 1 1 1] [1 0 1 0 0 0 1] [1 0 1 0 0 0 1] [1 0 1 0 0 0 1] [1 0 0 0 1 1 1] [1 0 0 0 0 0 1] [1 1 1 1 1 1 1]])

(print "maze:")
(print (get maze 0))
(print (get maze 1))
(print (get maze 2))
(print (get maze 3))
(print (get maze 4))
(print (get maze 5))
(print (get maze 6))
(print "")

(setv pacman [1 3])
(setv ghost [4 3])
(setv depth 0)

(print "pacman pos: " pacman)
(print "ghost pos: " ghost)
(print "")

(setv pacman_new (get_possible_moves pacman maze))
(print "Possible pacman moves: " pacman_new)
(print "")

(setv cost (minimax maze pacman ghost depth))
(print "Best pacman move and cost: " cost)
(print "")
