import pygame
import os
from constantes import *
from .robo import Robo
import random

class InimigoZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=4)
        self.direcao = random.choice([-2, -1, 0, 1, 2])
        self.velocidade_x = 3

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * self.velocidade_x

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()