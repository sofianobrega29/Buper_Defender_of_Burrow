import pygame
import random
from constantes import *# CLASSE BASE
class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image = pygame.image.load("sprites/jogador/buper.png")
        self.image = pygame.transform.scale(self.image, (84, 90)) 
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


# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image = pygame.image.load("sprites/jogador/tiro.png")
        self.image = pygame.transform.scale(self.image, (20, 40))  # amarelo

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()


# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 0, 0))  # vermelho

    def atualizar_posicao(self):
        raise NotImplementedError

class InimigoPadrao(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=6)

        self.image = pygame.image.load("sprites/inimigo/inimigo1.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (70, 120)) 

        self.rect = self.image.get_rect(center = (x, y))

        self.hitbox = pygame.Rect(
            self.rect.x + 15,
            self.rect.y + 20,
            54,
            70
        )

        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += random.choice([-2, -1, 1, 2])
        self.cont = 0

        if self.cont == 10:
            self.cont = 0

        if self.cont <= 0:
            if self.rect.x <= 0 or self.rect.x >= LARGURA - self.rect.width:
                self.direcao *= -1
                self.cont += 1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# ROBO EXEMPLO — ZigueZague
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

