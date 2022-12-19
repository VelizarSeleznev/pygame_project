# scenes.py
from classes import *


class Scenes(Vars):
    def change_scene(self, sceneNum):
        self.corSceneNum = sceneNum
        self.loop_running = False

    def load_0_MainMenu(self):
        # ПЕРЕМЕННЫЕ:
        all_sprites = pygame.sprite.Group()
        self.loop_running = True
        clock = pygame.time.Clock()

        # СЦЕНА:
        button = Button(self.sc, 100, 100, 300, 150, text='to test area', onClick=lambda: self.change_scene(99))

        # ЦИКЛ:
        while self.loop_running:
            clock.tick(self.fps)
            # обработка событий:
            events = pygame.event.get()
            for ev in events:
                if ev.type == pygame.QUIT:
                    self.loop_running = False  # выход из цикла отрисовки/логики текущего
                    self.prog_running = False
            # отрисовка кадра:
            self.sc.fill((0, 0, 0))
            pygame.draw.circle(self.sc, (255, 0, 0), (300, 300), 20)

            pygame_widgets.update(events)  # обновляем виджеты из модуля pygame_widgets
            pygame.display.update()

            button.listen(events)
            button.draw()

            pygame.display.flip()

    def load_99_TestArea(self):
        # ПЕРЕМЕННЫЕ:
        # all_sprites = pygame.sprite.Group()
        running = True

        clock = pygame.time.Clock()

        self.player = Player()
        # self.player.load_image('test_player.png', 100, 100)
        # all_sprites.add(self.player)

        cor_level = Level()
        cor_level.gen(3, 5)

        # СЦЕНА:
        print('test area!')
        # ЦИКЛ:
        while running:
            clock.tick(self.fps)
            # ОБРАБОТКА СОБЫТИЙ:
            # собственные ("общие") события:
            events = pygame.event.get()
            for ev in events:
                if ev.type == pygame.QUIT:
                    running = False  # выход из цикла отрисовки/логики текущего
                    self.prog_running = False
            # ОТРИСОВКА КАДРА:
            self.player.animate()
            self.sc.fill((0, 0, 200))
            # дергаем обновления-отрисовку объектов:
            cor_level.update(self.sc)
            self.player.update(self.sc, events)


            pygame.display.update()
            # all_sprites.draw(self.sc)
            # all_sprites.update()
            pygame.display.flip()
