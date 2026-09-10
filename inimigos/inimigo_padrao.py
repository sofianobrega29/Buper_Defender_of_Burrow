import pygame
import os
from constantes import *
from .robo import Robo

class InimigoPadrao(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=6)

        self.image = pygame.image.load(
            os.path.join(BASE_DIR, "sprites", "inimigo", "inimigo1.png")
        ).convert_alpha()

        self.image_redimensionada = pygame.transform.scale(self.image, (60, 180)) 
        self.image_direita = self.image_redimensionada
        self.image_esquerda = pygame.transform.flip(self.image_redimensionada, True, False)

        self.cont_andar = 0
        self.velocidade_andar_frame = 15

        self.rect = self.image_redimensionada.get_rect(center = (x, y))

        self.hitbox = pygame.Rect(
            self.rect.x + 15,
            self.rect.y + 20,
            54,
            70
        )

        self.direcao = 1

        self.image = self.image_direita

    def atualizar_andar(self):
        self.cont_andar += 1
        if self.cont_andar < self.velocidade_andar_frame:
            self.image = self.image_direita
        elif self.cont_andar < self.velocidade_andar_frame * 2:
            self.image = self.image_esquerda
        else:
            self.cont_andar = 0

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
        self.atualizar_andar()
        if self.rect.y > ALTURA:
            self.kill()