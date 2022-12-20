# classes.py
import pygame

from vars import *
# "Базовые" классы - модули, реализующие функции наследуемых классов.
# Проще говоря, это свойства, например, класс, наследуемый от Sprite
# будет иметь спрайт.


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


# ================== BASE CLASSES:
class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)


class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.DISPLAY_W)


class Auto(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset.x += 1


class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W = width
        self.DISPLAY_H = height
        self.CONST = vec(-(self.DISPLAY_W / 2 - self.player.rect.w), -(self.DISPLAY_H / 2 - self.player.rect.h))
        self.method = None

    def set_method(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()


class Sprite:
    def load_image(self, filepath, size_x=None, size_y=None):
        fullname = resource_path(filepath)
        # fullname = os.path.join('YLP-master\img', filepath)
        # if not os.path.isfile(fullname):
        #     logging.critical(f"Image file not found ('{fullname}')")
        #     sys.exit()
        self.img = pygame.image.load(fullname)

        if size_x and size_y:
            self.resize(size_x, size_y)

        self.rect = self.img.get_rect()

    def resize(self, new_width, new_height):
        self.img = pygame.transform.scale(self.img, (new_width, new_height))


class Collision:
    def __init__(self):
        pass
    # if collision:
    #    sprite1.rect.colliderect(sprite2.rect)


class ModuleManager:
    def init_modiles(self):
        base_classes = (Sprite, Collision)
        for cl in base_classes:
            if issubclass(type(self), cl):
                cl.__init__(self)


# ================== GAME CLASSES:

class Player(Sprite, ModuleManager):
    def __init__(self):
        # состояние
        self.directions_x = {-1: 'left', 1: 'right'}
        self.directions_y = {-1: 'up', 1: 'down'}
        self.direction = 'down'
        self.atk_state = 0
        self.moving = False
        self.hurt = False
        self.hp = 5
        self.dash = False
        self.jump = False
        self.current_anim = 0
        self.timer = pygame.time.get_ticks()
        self.atk_timer = pygame.time.get_ticks()
        self.dash_dir_x = 0
        self.dash_dir_y = 0
        self.rect = pygame.Rect((0, 0, 200, 200))

        # анимации
        my_spritesheet = Spritesheet('images/character/character.png')
        self.dash_len = 3
        self.dash_count = 0
        self.dash_need = 3
        self.atk_len = 30
        self.first_atk = 7
        self.second_atk = 7 + 6
        self.third_atk = 30
        self.walk_len = 12
        self.SB_len = 15
        self.all_dash_len = 16
        self.atk_up = []
        self.atk_down = []
        self.atk_right = []
        self.atk_left = []
        self.char = []
        self.char_back = []
        self.char_right = []
        self.char_left = []
        self.SB_down = []
        self.SB_right = []
        self.SB_left = []
        self.SB_up = []
        self.dash_back = []
        self.dash_up = []
        self.dash_right = []
        self.dash_left = []
        im = my_spritesheet.parse_sprite('spr_charstandside.png')
        self.stand = {'up': pygame.transform.scale2x(my_spritesheet.parse_sprite('spr_charstandback.png')),
                      'down': pygame.transform.scale2x(my_spritesheet.parse_sprite('spr_charstandfront.png')),
                      'right': pygame.transform.scale2x(im),
                      'left': pygame.transform.scale2x(pygame.transform.flip(im, True, False))}
        self.current_image = self.stand['down']
        for i in range(self.atk_len):
            self.atk_up.append(pygame.transform.scale2x(my_spritesheet.parse_sprite('5.' + str(i) + '.png')))
            self.atk_down.append(pygame.transform.scale2x(my_spritesheet.parse_sprite('4.' + str(i) + '.png')))
            im = pygame.transform.scale2x(my_spritesheet.parse_sprite('6.' + str(i) + '.png'))
            self.atk_right.append(im)
            self.atk_left.append(pygame.transform.flip(im, True, False))
        for i in range(self.walk_len):
            self.char.append(pygame.transform.scale2x(my_spritesheet.parse_sprite('1.' + str(i) + '.png')))
            self.char_back.append(pygame.transform.scale2x(my_spritesheet.parse_sprite('2.' + str(i) + '.png')))
            im = pygame.transform.scale2x(my_spritesheet.parse_sprite(str(i) + '.png'))
            self.char_right.append(im)
            self.char_left.append(pygame.transform.flip(im, True, False))
        for i in range(self.SB_len):
            self.SB_down.append(pygame.transform.scale2x(my_spritesheet.parse_sprite('10.' + str(i) + '.png')))
            im = pygame.transform.scale2x(my_spritesheet.parse_sprite('12.' + str(i) + '.png'))
            self.SB_right.append(im)
            self.SB_left.append(pygame.transform.flip(im, True, False))
            self.SB_up.append(pygame.transform.scale2x(my_spritesheet.parse_sprite('11.' + str(i) + '.png')))
        for i in range(self.all_dash_len):
            self.dash_up.append(pygame.transform.scale2x(my_spritesheet.parse_sprite('7.' + str(i) + '.png')))
            self.dash_back.append(pygame.transform.scale2x(my_spritesheet.parse_sprite('8.' + str(i) + '.png')))
            im = pygame.transform.scale2x(my_spritesheet.parse_sprite('9.' + str(i) + '.png'))
            self.dash_right.append(im)
            self.dash_left.append(pygame.transform.flip(im, True, False))
        # инициализация:
        self.init_modiles()
        self.dash_speed = 0
        self.pos_x = self.pos_y = 0
        self.en_x = self.en_y = 0  # инерция
        self.max_speed = 7
        self.en_delta = 0.5
        self.braking = 0.8  # скорость торможения
        self.move_y = self.move_x = 0

        # преднастройка модулей:
        #

    def set_camera(self, camera):
        self.camera = camera

    def get_image(self):
        # default (32, 64)

        surf = pygame.Surface((400, 400), pygame.SRCALPHA, 32).convert_alpha()
        if self.current_image in self.char or self.current_image in self.char_back\
                or self.current_image in self.char_left:
            surf.blit(self.current_image, (200 - 12 * 2, 200 - 35))
        elif self.current_image in self.char_right:
            surf.blit(self.current_image, (200 - 20 * 2, 200 - 35))
        elif self.current_image in self.atk_up:
            surf.blit(self.current_image, (200 - 31 * 2, 200 - 61 * 2))
        elif self.current_image in self.atk_down:
            surf.blit(self.current_image, (200 - 22 * 2, 200 - 22 * 2))
        elif self.current_image in self.atk_right:
            surf.blit(self.current_image, (200 - 40 * 2, 200 - 34 * 2))
        elif self.current_image in self.atk_left:
            surf.blit(self.current_image, (200 - 97 * 2 + 24 * 2, 200 - 34 * 2))
        elif self.current_image in self.dash_right:
            surf.blit(self.current_image, (200 - 44, 200 - 30))
        elif self.current_image in self.dash_left:
            surf.blit(self.current_image, (200 - 44, 200 - 30))
        elif self.current_image in self.dash_up:
            surf.blit(self.current_image, (200 - 20, 200 - 32))
        elif self.current_image in self.dash_back:
            surf.blit(self.current_image, (200 - 25, 200 - 32))
        else:
            surf.blit(self.current_image, (200 - 8 * 2, 200 - 16 * 2))
        return surf

    def atk_image(self):
        if pygame.time.get_ticks() - self.timer > 60:
            self.current_anim += 1
            self.current_anim %= self.atk_len
            self.timer = pygame.time.get_ticks()
            if self.direction == 'up':
                self.current_image = self.atk_up[self.current_anim]
            elif self.direction == 'down':
                self.current_image = self.atk_down[self.current_anim]
            elif self.direction == 'right':
                self.current_image = self.atk_right[self.current_anim]
            else:
                self.current_image = self.atk_left[self.current_anim]

    def walk_image(self):
        if pygame.time.get_ticks() - self.timer > 100:
            self.current_anim += 1
            self.current_anim %= self.walk_len
            self.timer = pygame.time.get_ticks()
            if self.direction == 'up':
                self.current_image = self.char_back[self.current_anim]
            elif self.direction == 'down':
                self.current_image = self.char[self.current_anim]
            elif self.direction == 'right':
                self.current_image = self.char_right[self.current_anim]
            else:
                self.current_image = self.char_left[self.current_anim]

    def dash_image(self):
        if self.dash_count < self.dash_need:
            self.dash_speed = self.max_speed * 3
            if pygame.time.get_ticks() - self.timer > 30:
                self.current_anim += 1
                self.current_anim %= self.dash_len
                self.timer = pygame.time.get_ticks()
                if self.direction == 'up':
                    self.current_image = self.dash_back[self.current_anim]
                elif self.direction == 'down':
                    self.current_image = self.dash_up[self.current_anim]
                elif self.direction == 'right':
                    self.current_image = self.dash_right[self.current_anim]
                else:
                    self.current_image = self.dash_left[self.current_anim]
                self.dash_count += 1
        else:
            if pygame.time.get_ticks() - self.timer > 50:
                self.current_anim += 1
                self.dash_count += 1
                if self.current_anim < self.all_dash_len:
                    self.dash_speed *= 0.7
                    self.dash_speed = int(self.dash_speed)
                    if self.dash_speed <= 1:
                        self.dash_speed = 0
                    self.timer = pygame.time.get_ticks()
                    if self.direction == 'up':
                        self.current_image = self.dash_back[self.current_anim]
                    elif self.direction == 'down':
                        self.current_image = self.dash_up[self.current_anim]
                    elif self.direction == 'right':
                        self.current_image = self.dash_right[self.current_anim]
                    else:
                        self.current_image = self.dash_left[self.current_anim]
                else:
                    self.walk_image()
                    self.dash = False
                    self.dash_count = 0
                    return

    def animate(self):
        if self.atk_state > 0:
            if self.current_anim >= self.first_atk and self.atk_state > 1:
                if self.current_anim >= self.second_atk and self.atk_state > 2:
                    if self.current_anim >= self.third_atk - 1:
                        self.current_anim = 0
                        self.atk_state = 0
                        self.atk_timer = pygame.time.get_ticks()
                    else:
                        self.atk_image()
                else:
                    if self.current_anim >= self.second_atk and self.atk_state == 2 \
                            and pygame.time.get_ticks() - self.timer >= 100:
                        self.current_anim = 0
                        self.atk_state = 0
                        self.atk_timer = pygame.time.get_ticks()
                    elif self.current_anim <= self.second_atk:
                        self.atk_image()
            else:
                if self.current_anim >= self.first_atk and pygame.time.get_ticks() - self.timer >= 100:
                    self.current_anim = 0
                    self.atk_state = 0
                    self.atk_timer = pygame.time.get_ticks()
                elif self.current_anim <= self.first_atk:
                    self.atk_image()
        elif self.dash:
            self.dash_image()
        elif self.moving:
            self.walk_image()
        else:
            self.current_image = self.stand[self.direction]

    def move(self, right, down):
        if self.dash:
            self.en_x = self.dash_speed * self.dash_dir_x
            self.en_y = self.dash_speed * self.dash_dir_y
        else:
            if abs(self.en_x) < self.max_speed:
                self.en_x += self.en_delta * right
            else:
                if self.en_x > 0:
                    self.en_x = self.max_speed
                else:
                    self.en_x = self.max_speed * -1
            if abs(self.en_y) < self.max_speed:
                self.en_y += self.en_delta * down
            else:
                if self.en_y > 0:
                    self.en_y = self.max_speed
                else:
                    self.en_y = self.max_speed * -1

    def update(self, scene, events):
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        scene.blit(self.get_image(), (self.pos_x - self.camera.offset.x, self.pos_y - self.camera.offset.y))
        # (self.pos_x, self.pos_y))

        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    if pygame.time.get_ticks() - self.atk_timer >= 150:
                        if self.atk_state == 0:
                            self.current_anim = 0
                        self.atk_state += 1
                        self.moving = False
                        self.move_y = 0
                        self.move_x = 0
                if ev.key == pygame.K_LSHIFT:
                    if self.dash_count <= 10:
                        self.dash_count = 0
                        self.dash = True
                        self.current_anim = 0
                        if not self.moving:
                            if self.direction == 'up':
                                self.dash_dir_y = -1
                                self.dash_dir_x = 0
                            elif self.direction == 'down':
                                self.dash_dir_y = 1
                                self.dash_dir_x = 0
                            elif self.direction == 'right':
                                self.dash_dir_x = 1
                                self.dash_dir_y = 0
                            else:
                                self.dash_dir_x = -1
                                self.dash_dir_y = 0
                        else:
                            self.dash_dir_y = self.move_y
                            self.dash_dir_x = self.move_x
                if ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    if self.atk_state == 0:
                        self.move_y = -1
                elif ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    if self.atk_state == 0:
                        self.move_y = 1
                if ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    if self.atk_state == 0:
                        self.move_x = -1
                elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    if self.atk_state == 0:
                        self.move_x = 1
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    self.move_y = 0
                if ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    self.move_y = 0
                if ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    self.move_x = 0
                if ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    self.move_x = 0
        if self.move_y:
            self.moving = True
            self.direction = self.directions_y[self.move_y]
        if self.move_x:
            self.moving = True
            self.direction = self.directions_x[self.move_x]
        if not self.move_x and not self.move_y:
            self.moving = False

        self.move(self.move_x, self.move_y)
        self.pos_x += self.en_x
        if not self.move_x:
            if self.en_x > self.braking:
                self.en_x -= self.braking
            elif self.en_x < self.braking * -1:
                self.en_x += self.braking
            else:
                self.en_x = 0
        self.pos_y += self.en_y
        if not self.move_y:
            if self.en_y > self.braking:
                self.en_y -= self.braking
            elif self.en_y < self.braking * -1:
                self.en_y += self.braking
            else:
                self.en_y = 0


class Level:
    def __init__(self):
        self.raw_map = []
        self.camera = None
        stone = Sprite()
        stone.load_image("test_wall_block.png", 100, 100)
        self.stone_image = stone.img
        self.map = None

    def gen(self, mappath):
        with open(mappath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = list(line.strip('\n'))
                self.raw_map.append(line)
        self.map = pygame.surface.Surface((len(self.raw_map) * 100, len(self.raw_map[0]) * 100))
        for i, a in enumerate(self.raw_map):
            for j, b in enumerate(a):
                if self.raw_map[i][j] == '0':
                    self.map.blit(self.stone_image, (100 * i, 100 * j))

    def update(self, scene):
        scene.blit(self.map, (-self.camera.offset.x, -self.camera.offset.y))
        scene.blit(self.map, (-self.camera.offset.x, -self.camera.offset.y))

    def set_camera(self, camera):
        self.camera = camera
