# additional.py
from scenes import *


class Game(Scenes):
    def mainloop(self):
        logging.info("start the main scene switching loop")

        # window initialization:
        pygame.init()
        pygame.display.set_caption(title)
        if self.sett_fullscreen:
            self.sc = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.sc = pygame.display.set_mode((width, height))
        while self.prog_running:  # scene switching cycle
            if self.corSceneNum == 0:
                self.load_0_MainMenu()
            elif self.corSceneNum == 1:
                self.load_1_endscreen()
            elif self.corSceneNum == 99:
                self.load_99_TestArea()
            print(self.corSceneNum)
        pygame.quit()
