import os
import pygame
from constantes import BASE_DIR, ALTURA

class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y, valor=1):
        super().__init__()

        self.valor = valor
        caminho = os.path.join(
            BASE_DIR, "assets", "sprites", "moeda.png"
        )

        try:
            imagem = pygame.image.load(caminho).convert_alpha()
            self.image = pygame.transform.scale(imagem, (55, 55))
        except (pygame.error, OSError):
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 210, 45), (12, 12), 11)
            pygame.draw.circle(self.image, (255, 245, 150), (12, 12), 11, 2)
            pygame.draw.circle(self.image, (180, 120, 20), (12, 12), 5)

        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Acompanha a rolagem do cenario e some ao sair da tela.
        self.rect.y += 2
        if self.rect.top > ALTURA:
            self.kill()
