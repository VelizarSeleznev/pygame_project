# something.py
from additional import *

logging.basicConfig(level=logging.INFO, filename="journal.log", filemode="w")

# STARTING THE PROGRAM:
if __name__ == '__main__':
    g = Game()
    g.mainloop()
