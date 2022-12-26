# vars.py
import os
import sys
import json
import random

import logging

import pygame
import pygame_widgets
from pygame_widgets.button import Button
import pygame as p
from abc import ABC, abstractmethod

from spritesheet import Spritesheet

# GLOBAL:
g = None  # (Game) game unit
corSceneNum = 0  # изначально 0 - главное меню
corLevel = None  # (Level) current game level
vec = p.math.Vector2
width, height = 1920, 800


class Vars:
    def __init__(self):
        self.camera = None
        self.fps = 60
        self.width, self.height = width, height
        self.title = 'my_title'
        self.sc = None  # window
        self.corSceneNum = 0  # current scene number
        self.player = None
        self.joysticks = {}

        self.prog_running = True  # running program (scene switching loop)
        self.loop_running = True  # running render/logic loop
