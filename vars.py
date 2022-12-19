# vars.py
import os
import sys
import json

import logging

import pygame
import pygame_widgets
from pygame_widgets.button import Button

from spritesheet import Spritesheet

# GLOBAL:
g = None  # (Game) game unit
corSceneNum = 0  # изначально 0 - главное меню
corLevel = None  # (Level) current game level


class Vars:
    def __init__(self):

        self.fps = 60
        self.width, self.height = 1920, 800
        self.title = 'my_title'
        self.sc = None  # window
        self.corSceneNum = 0  # current scene number
        self.player = None

        self.prog_running = True  # running program (scene switching loop)
        self.loop_running = True  # running render/logic loop
