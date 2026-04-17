# The size of a chip, everything else is scaled from it
# The board is 13.5*15.5 with borders and 11.5*13.5 without it
chip_size = 50

# Pygame graphics (Needed for human players)
graphics = True

# Moves per second (zero for off, can't be higher than fps)
# Should only be used in bot vs bot
mps = 0
fps = 60
summation = 1 # How often the wins get summed

# Who plays as White and Black
B_Player = "hard_bot"
W_Player = "human"

Height = 14.5*chip_size
Width = 14.5*chip_size