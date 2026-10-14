import os
import pygame
from inimigos.robo import Entidade
from constantes import BASE_DIR

_CACHE = {}


def _imagem_tiro(cor):
    """Carrega o sprite uma unica vez por cor (antes lia o disco a cada disparo)."""
    if cor not in _CACHE:
        caminho = os.path.join(BASE_DIR, "sprites", "jogador", "tiro.png")
        imagem = pygame.image.load(caminho).convert_alpha()
        imagem = pygame.transform.scale(imagem, (20, 40))

        if cor != (255, 255, 255):
            # RGB_MULT tinge sem alterar a transparencia do sprite.
            imagem.fill((*cor, 255), special_flags=pygame.BLEND_RGB_MULT)

        _CACHE[cor] = imagem

    return _CACHE[cor]


class Tiro(Entidade):
    def __init__(self, x, y, dano=1, cor=(255, 255, 255)):
        super().__init__(x, y, 10)
        self.image = _imagem_tiro(tuple(cor))
        self.rect = self.image.get_rect(center=(x, y))
        self.dano = dano

    def update(self):
        self.rect.y -= self.velocidade

        if self.rect.bottom < 0:
            self.kill()
