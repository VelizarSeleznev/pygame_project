# additional.py
from scenes import *


class Level:
    def __init__(self):
        x, y = 10, 5
        a = [[None] * x for i in range(y)]


class Game(Scenes):
    def mainloop(self):
        logging.info("start the main scene switching loop")

        # window initialization:
        pygame.init()
        pygame.display.set_caption(self.title)
        self.sc = pygame.display.set_mode((self.width, self.height))

        while self.prog_running:  # scene switching cycle
            if self.corSceneNum == 0:
                self.load_0_MainMenu()
            elif self.corSceneNum == 99:
                self.load_99_TestArea()
        pygame.quit()
