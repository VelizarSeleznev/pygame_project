import pygame
from spritesheet import Spritesheet


class Player:
    def __init__(self):
        # состояние
        self.direcitons = ['up', 'down', 'left', 'right']
        self.direction = 'down'
        self.atk_state = 0
        self.move = False
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
        elif self.move:
            self.walk_image()
        else:
            self.current_image = self.stand[self.direction]
