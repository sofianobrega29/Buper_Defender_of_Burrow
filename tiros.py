import pygame
from inimigos.robo import Entidade
import os
from constantes import *

class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image = pygame.image.load(
            os.path.join(BASE_DIR, "sprites", "jogador", "tiro.png")
        )
        self.image = pygame.transform.scale(self.image, (20, 40))  # amarelo

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()
