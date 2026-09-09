import pygame
import os
from constantes import *
from .robo import Robo

class InimigoVeloz(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=8)

        self.image = pygame.image.load(
            os.path.join(BASE_DIR, "sprites", "inimigo", "inimigo1.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 90)) 

        self.rect = self.image.get_rect(center = (x, y))

        self.hitbox = pygame.Rect(
            self.rect.x + 15,
            self.rect.y + 20,
            37,
            35
        )

        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        '''self.rect.x += random.choice([-2, -1, 1, 2])'''
        self.cont = 0

        if self.cont == 10:
            self.cont = 0

        if self.cont <= 0:
            if self.rect.x <= 0 or self.rect.x >= LARGURA - self.rect.width:
                self.direcao *= -1
                self.cont += 1

    def aumentar_velocidade(self):
        self.velocidade += 2

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()