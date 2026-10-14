import pygame
from constantes import LARGURA, ALTURA


class BolaInimiga(pygame.sprite.Sprite):
    """Projetil disparado pelo Atirador. Some ao sair da tela."""

    def __init__(self, x, y, alvo_x, alvo_y, velocidade=6):
        super().__init__()
        self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (150, 40, 200), (11, 11), 11)
        pygame.draw.circle(self.image, (230, 150, 255), (11, 11), 11, 2)
        pygame.draw.circle(self.image, (255, 255, 255), (8, 8), 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x, self.pos_y = float(x), float(y)

        dx, dy = alvo_x - x, alvo_y - y
        dist = max(1, (dx * dx + dy * dy) ** 0.5)
        self.vx = dx / dist * velocidade
        self.vy = dy / dist * velocidade

    def update(self):
        self.pos_x += self.vx
        self.pos_y += self.vy
        self.rect.center = (round(self.pos_x), round(self.pos_y))
        if (
            self.rect.top > ALTURA or self.rect.bottom < 0
            or self.rect.right < 0 or self.rect.left > LARGURA
        ):
            self.kill()
