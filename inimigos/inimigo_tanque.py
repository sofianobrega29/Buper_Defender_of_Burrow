import pygame
from constantes import ALTURA
from .robo import Robo
from ._sprite import Animado, carregar_frames


class InimigoTanque(Animado, Robo):
    """Grande e lento, aguenta 3 tiros de dano 1."""
    valor_pontos = 40
    valor_moedas = 2

    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2)
        self.iniciar_animacao(
            carregar_frames("tanque", (120, 165), cor=(120, 150, 255)), intervalo=9
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(0, 0, 90, 115)
        self.hitbox.center = self.rect.center
        self.vida_maxima = 6
        self.vida = self.vida_maxima

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.hitbox.center = self.rect.center

    def update(self):
        self.atualizar_posicao()
        self.animar()
        if self.rect.y > ALTURA:
            self.kill()
