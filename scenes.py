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
                if ev.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(ev.device_index)
                    self.joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick {joy.get_instance_id()} connencted")

                if ev.type == pygame.JOYDEVICEREMOVED:
                    del self.joysticks[ev.instance_id]
                    print(f"Joystick {ev.instance_id} disconnected")
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
        self.camera = Camera(self.player)
        follow = Follow(self.camera, self.player)
        self.camera.set_method(follow)
        self.player.set_camera(self.camera)
        if self.joysticks:
            self.player.set_joystick(True)
        # self.player.load_image('test_player.png', 100, 100)
        # all_sprites.add(self.player)

        cor_level = Level()
        cor_level.set_camera(self.camera)
        cor_level.gen('maps/level3.map')

        # СЦЕНА:
        print('test area!')
        stones = cor_level.get_blocks()
        self.player.timer = pygame.time.get_ticks()
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
                if ev.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(ev.device_index)
                    self.joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick {joy.get_instance_id()} connencted")

                if ev.type == pygame.JOYDEVICEREMOVED:
                    del self.joysticks[ev.instance_id]
                    print(f"Joystick {ev.instance_id} disconnected")
            # ОТРИСОВКА КАДРА:
            self.player.animate()
            self.sc.fill((0, 0, 0))
            # дергаем обновления-отрисовку объектов:
            self.player.update(self.sc, events)
            self.player.collide(stones)
            self.camera.scroll()
            cor_level.update(self.sc)

            pygame.display.update()
            # all_sprites.draw(self.sc)
            # all_sprites.update()
            pygame.display.flip()
