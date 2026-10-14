import pygame
from constantes import ALTURA
from .robo import Robo
from ._sprite import Animado, carregar_frames


class InimigoPadrao(Animado, Robo):
    valor_pontos = 10

    def __init__(self, x, y):
        super().__init__(x, y, velocidade=6)
        self.iniciar_animacao(carregar_frames("padrao", (60, 180)), intervalo=6)
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(0, 0, 54, 70)
        self.hitbox.center = self.rect.center

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.hitbox.center = self.rect.center

    def update(self):
        self.atualizar_posicao()
        self.animar()
        if self.rect.y > ALTURA:
            self.kill()
