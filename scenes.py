# scenes.py

from classes import *
from generator import create_map


class Scenes(Vars):
    ### Вспомогательные функции:
    def exit(self):
        ##### тут сохранение данных #####
        cfg["screen"]["width"] = str(width)
        cfg["screen"]["height"] = str(height)
        cfg["screen"]["fullscreen"] = str(self.sett_fullscreen)
        print(self.sett_fullscreen)
        with open('settings.ini', 'w') as configfile:
            cfg.write(configfile)
        self.loop_running = False
        self.prog_running = False

    def settings_apply(self):
        global width
        global height

        if self.pre_sett_fullscreen:
            self.sc = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.sett_fullscreen = 1
        else:
            if self.dropdown_res.getSelected() != None:
                selected_res = self.dropdown_res.getSelected().split('x')
                width = int(selected_res[0])
                height = int(selected_res[1])
            # self.sc = pygame.display.set_mode((width, height), )
            pygame.transform.scale(self.sc, (width, height))
            pygame.display.update()

            self.sett_fullscreen = 0
            # if self.dropdown_res.getSelected() != None:
            self.change_scene(0)

    def change_scene(self, sceneNum):
        self.corSceneNum = sceneNum
        self.loop_running = False

    def show_settings(self, var=None):
        if var != None:
            self.show_sett = var
        else:
            self.show_sett = not (self.show_sett)

        if self.show_sett:
            self.dropdown_res.show()
            self.toggle_fullscreen.show()
            self.apply_settings_btn.show()
        else:
            self.dropdown_res.hide()
            self.toggle_fullscreen.hide()
            self.apply_settings_btn.hide()

    def toggle_fullscreen_clb(self):
        if self.pre_sett_fullscreen:
            self.pre_sett_fullscreen = 0
        else:
            self.pre_sett_fullscreen = 1
        # self.toggle_fullscreen.inactiveColour((200, 50, 0))
        # ТУТ НУЖНО КАК ТО ПОКАЗАТЬ, ЧТО ВЫБРАН/СНЯТ ПУНКТ "ПОЛНЫЙ ЭКРАН"

    ### Функции-загрузки сцен:
    def load_0_MainMenu(self):
        logging.info("loading main menu")
        # ПЕРЕМЕННЫЕ:
        all_sprites = pygame.sprite.Group()
        self.loop_running = True
        clock = pygame.time.Clock()
        self.show_sett = False
        self.pre_sett_fullscreen = self.sett_fullscreen

        # СЦЕНА:
        # https://www.wallpaperbetter.com/ru/hd-wallpaper-pztie <- фоны брал отсюда
        try:
            bg_image = pygame.image.load('images/bg/bg_' + str(width) + 'x' + str(height) + '_16x9.jpg')
        except FileNotFoundError:
            bg_image = pygame.image.load('images/bg/bg_1920x1080_16x9.jpg')
        bg_image_rect = bg_image.get_rect()  # (0, 0, 1920, 1080)
        self.button_test = Button(self.sc, 10, 10, 100, 40, text='to test area', onClick=lambda: self.change_scene(99))
        #  self.button_continue = Button(self.sc, 10, 10, 100, 40, text='продолжить', onClick=lambda: print('продолжить'))
        self.button_run = Button(self.sc, int(width / 2 - 50), 10 + 50, 100, 40, text='забег',
                                 onClick=lambda: print('забег'))
        self.button_settings = Button(self.sc, int(width / 2 - 50), 10 + 50 * 2, 100, 40, text='настройки',
                                      onClick=lambda: self.show_settings())
        self.button_exit = Button(self.sc, int(width / 2 - 50), 10 + 50 * 3, 100, 40, text='выйти',
                                  onClick=lambda: self.exit())

        self.dropdown_res = Dropdown(self.sc, int(((width / 4) * 3 - 50)), 60, 140, 30, name='select resolution',
                                     choices=sc_resolution, borderRadius=3, colour=pygame.Color('grey'),
                                     values=sc_resolution, direction='down', textHAlign='left')
        # self.toggle_fullscreen = Toggle(self.sc, int(((width/4)*3 - 20)), 100, 40, 20)
        self.toggle_fullscreen = Button(self.sc, int(((width / 4) * 3 + 50 - 15)), 100, 30, 30, text='X',
                                        onClick=lambda: self.toggle_fullscreen_clb())
        self.apply_settings_btn = Button(self.sc, int(((width / 4) * 3 - 50)), 160, 100, 30, text='применить',
                                         onClick=lambda: self.settings_apply())

        self.show_settings(False)
        # ЦИКЛ:
        logging.info("start main menu cycle")
        while self.loop_running:
            clock.tick(fps)
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
            self.sc.blit(bg_image, bg_image_rect)

            pygame_widgets.update(events)  # обновляем виджеты из модуля pygame_widgets
            pygame.display.update()

            pygame.display.flip()

        # чистим "статические" переменные (да, в питоне нет статики, но по логике этой функции это статика, смирись)
        self.button_test.disable()
        self.button_test.hide()
        del self.button_test
        self.button_run.disable()
        self.button_run.hide()
        del self.button_run
        self.button_settings.disable()
        self.button_settings.hide()
        del self.button_settings
        self.button_exit.disable()
        self.button_exit.hide()
        del self.button_exit
        self.dropdown_res.disable()
        self.dropdown_res.hide()
        del self.dropdown_res
        self.toggle_fullscreen.disable()
        self.toggle_fullscreen.hide()
        del self.toggle_fullscreen
        self.apply_settings_btn.disable()
        self.apply_settings_btn.hide()
        del self.apply_settings_btn

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
        maps_n = create_map()
        cor_level = Level()
        cor_level.set_camera(self.camera)
        cor_level.gen('maps/level' + str(maps_n) + '.map')
        self.player.set_pos(cor_level.get_pos())

        # СЦЕНА:
        print('test area!')
        stones = cor_level.get_blocks()
        self.player.timer = pygame.time.get_ticks()
        # ЦИКЛ:
        while running:
            clock.tick(fps)
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
            pygame.display.flip()
        maps_path = './maps'
        map_format = 'level{}.map'
        image_format = 'level{}.png'
        maps_files = [
            f for f in os.listdir(maps_path)
            if f.endswith('.map') and os.path.isfile(os.path.join(maps_path, f))
        ]
        maps_count = len(maps_files)
        for i in range(maps_count):
            os.remove(os.path.join(maps_path, map_format.format(i + 1)))
            os.remove(os.path.join(maps_path, image_format.format(i + 1)))
