# classes.py
from vars import *
# "базовые" классы -  модули, реализующие функции наследуемых классво.
# проще говоря, это свойства, например, класс, наследуемый от Sprite
# будет иметь спрайт.


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


# ================== BASE CLASSES:
class Sprite:
    def __init__(self):
        # состояние
        self.direcitons = ['up', 'down', 'left', 'right']
        self.direction = 'down'
        self.atk_state = 0
        self.moving = False
        self.hurt = False
        self.hp = 5
        self.dash = False
        self.jump = False
        self.current_anim = 0
        self.timer = pygame.time.get_ticks()

        # анимации
        my_spritesheet = Spritesheet('character.png')
        self.atk_len = 30
        self.first_atk = 7
        self.second_atk = 7 + 7
        self.third_atk = 16 + 7 + 7
        self.walk_len = 12
        self.SB_len = 15
        self.dash_len = 16
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
        self.stand = {'up': my_spritesheet.parse_sprite('spr_charstandback.png'),
                      'down': my_spritesheet.parse_sprite('spr_charstandfront.png'),
                      'right': im, 'left': pygame.transform.flip(im, True, False)}
        self.current_image = self.stand['down']
        for i in range(self.atk_len):
            self.atk_up.append(my_spritesheet.parse_sprite('5.' + str(i) + '.png'))
            self.atk_down.append(my_spritesheet.parse_sprite('4.' + str(i) + '.png'))
            im = my_spritesheet.parse_sprite('6.' + str(i) + '.png')
            self.atk_right.append(im)
            self.atk_left.append(pygame.transform.flip(im, True, False))
        for i in range(self.walk_len):
            self.char.append(my_spritesheet.parse_sprite('1.' + str(i) + '.png'))
            self.char_back.append(my_spritesheet.parse_sprite('2.' + str(i) + '.png'))
            im = my_spritesheet.parse_sprite(str(i) + '.png')
            self.char_right.append(im)
            self.char_left.append(pygame.transform.flip(im, True, False))
        for i in range(self.SB_len):
            self.SB_down.append(my_spritesheet.parse_sprite('10.' + str(i) + '.png'))
            im = my_spritesheet.parse_sprite('12.' + str(i) + '.png')
            self.SB_right.append(im)
            self.SB_left.append(pygame.transform.flip(im, True, False))
            self.SB_up.append(my_spritesheet.parse_sprite('11.' + str(i) + '.png'))
        for i in range(self.dash_len):
            self.dash_up.append(my_spritesheet.parse_sprite('7.' + str(i) + '.png'))
            self.dash_back.append(my_spritesheet.parse_sprite('8.' + str(i) + '.png'))
            im = my_spritesheet.parse_sprite('9.' + str(i) + '.png')
            self.dash_right.append(im)
            self.dash_left.append(pygame.transform.flip(im, True, False))

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
        # инициализация:
        self.init_modiles()

        self.pos_x = self.pos_y = 0
        self.en_x = self.en_y = 0  # инерция
        self.max_speed = 7
        self.en_delta = 0.5
        self.braking = 0.8  # скорость торможения
        self.move_y = self.move_x = 0

        # преднастройка модулей:
        #

    def get_image(self):
        surf = pygame.Surface((200, 200), pygame.SRCALPHA, 32).convert_alpha()
        if self.current_image in self.char or self.current_image in self.char_back\
                or self.current_image in self.char_left:
            surf.blit(self.current_image, (100 - 12, 100 - 35 // 2))
        elif self.current_image in self.char_right:
            surf.blit(self.current_image, (100 - 20, 100 - 35 // 2))
        elif self.current_image in self.atk_up:
            surf.blit(self.current_image, (100 - 31, 100 - 61))
        elif self.current_image in self.atk_down:
            surf.blit(self.current_image, (100 - 22, 100 - 22))
        elif self.current_image in self.atk_right:
            surf.blit(self.current_image, (100 - 40, 100 - 34))
        elif self.current_image in self.atk_left:
            surf.blit(self.current_image, (100 - 97 + 24, 100 - 34))
        else:
            surf.blit(self.current_image, (100 - 8, 100 - 16))
        return surf

    def atk_image(self):
        if pygame.time.get_ticks() - self.timer > 35:
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
        if pygame.time.get_ticks() - self.timer > 40:
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

    def animate(self):
        if self.atk_state > 0:
            if self.current_anim >= self.first_atk and self.atk_state > 1:
                if self.current_anim >= self.second_atk and self.atk_state > 2:
                    if self.current_anim >= self.third_atk - 1:
                        self.current_anim = 0
                        self.atk_state = 0
                    else:
                        self.atk_image()
                else:
                    if self.current_anim >= self.second_atk:
                        self.current_anim = 0
                        self.atk_state = 0
                    else:
                        self.atk_image()
            else:
                if self.current_anim >= self.first_atk:
                    self.current_anim = 0
                    self.atk_state = 0
                else:
                    self.atk_image()
        elif self.dash:
            pass
        elif self.moving:
            self.walk_image()
        else:
            self.current_image = self.stand[self.direction]

    def move(self, right, down):
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

        scene.blit(self.get_image(), (self.pos_x, self.pos_y))  # (self.pos_x, self.pos_y))

        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    if self.atk_state == 0:
                        self.current_anim = 0
                    self.atk_state += 1
                    self.moving = False
                    self.move_y = 0
                    self.move_x = 0
                if ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    if self.atk_state == 0:
                        self.move_y = -1
                        self.moving = True
                        self.direction = 'up'
                elif ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    if self.atk_state == 0:
                        self.move_y = 1
                        self.moving = True
                        self.direction = 'down'
                if ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    if self.atk_state == 0:
                        self.moving = True
                        self.direction = 'left'
                        self.move_x = -1
                elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    if self.atk_state == 0:
                        self.moving = True
                        self.direction = 'right'
                        self.move_x = 1
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    self.move_y = 0
                    self.moving = False
                if ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    self.move_y = 0
                    self.moving = False
                if ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    self.move_x = 0
                    self.moving = False
                if ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    self.move_x = 0
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
        title = ''
        self.mapL1 = []

    def gen(self, x, y):
        self.mapL1 = [[Sprite()] * x for i in range(y)]
        for i in self.mapL1:
            for j in i:
                j.load_image("test_wall_block.png", 100, 100)

    def update(self, scene):
        n_i = 0
        for i in self.mapL1:
            n_j = 0
            for j in i:
                scene.blit(j.img, (100*n_i, 100*n_j))
                n_j += 1
            n_i += 1

'''
class Camera:
    def __init__(self):
        self.dx = self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, rect):
        self.dx = -(rect.x + rect.w // 2 - 1920 // 2)
        self.dy = -(rect.y + rect.h // 2 - 800 // 2)
        print(self.dx, self.dy)
'''