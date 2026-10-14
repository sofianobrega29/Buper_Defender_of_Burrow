import random
from constantes import LARGURA, ALTURA
from .robo import Robo
from ._sprite import Animado, carregar_frames


class InimigoZigueZague(Animado, Robo):
    valor_pontos = 15

    def __init__(self, x, y):
        super().__init__(x, y, velocidade=4)
        self.iniciar_animacao(carregar_frames("ziguezague", (42, 105)), intervalo=5)
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.copy()
        self.direcao = random.choice([-2, -1, 1, 2])
        self.velocidade_x = 3

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * self.velocidade_x

        # Quica nas laterais (e garante que nao fica preso fora da tela).
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direcao = abs(self.direcao)
        elif self.rect.right >= LARGURA:
            self.rect.right = LARGURA
            self.direcao = -abs(self.direcao)

        self.hitbox.center = self.rect.center

    def update(self):
        self.atualizar_posicao()
        self.animar()
        if self.rect.y > ALTURA:
            self.kill()
