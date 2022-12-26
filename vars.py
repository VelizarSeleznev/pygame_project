# vars.py
import os
import sys
import json

import logging
import configparser

import pygame
import pygame_widgets
from pygame_widgets.button import Button
import pygame as p
from abc import ABC, abstractmethod

from spritesheet import Spritesheet

# GLOBAL:
cfg = configparser.ConfigParser()
cfg.read("settings.ini")
g = None  # (Game) game unit
corSceneNum = 0  # изначально 0 - главное меню
corLevel = None  # (Level) current game level
vec = p.math.Vector2
fps = int(cfg["screen"]["fps"])
width, height = int(cfg["screen"]["width"]), int(cfg["screen"]["height"])
block_width, block_height = 150, 150  # размеры одной клетки
title = cfg["screen"]["title"]

class Vars:
    def __init__(self):
        self.sc = None  # window
        self.corSceneNum = 0  # current scene number
        self.joysticks = {}
        self.prog_running = True  # running program (scene switching loop)
        self.loop_running = True  # running render/logic loop