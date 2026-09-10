import pygame
from inimigos.robo import Entidade
from constantes import *
import os

class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image = pygame.image.load(
            os.path.join(BASE_DIR, "sprites", "jogador", "buper.png")
        )
        self.image = pygame.transform.scale(self.image, (80, 95)) 
        self.rect = self.image.get_rect(center=(x, y))

        self.vida = 5
        self.eliminacoes = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.rect.height))
