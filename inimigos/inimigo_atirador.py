import random
import pygame
from constantes import LARGURA, ALTURA, TOPO_HUD
from .robo import Robo
from ._sprite import Animado, carregar_frames
from .bola_inimiga import BolaInimiga


class InimigoAtirador(Animado, Robo):
    """Desce ate a parte de cima da tela, para e atira bolas no jogador.
    Depois de um tempo foge para baixo."""
    valor_pontos = 35
    valor_moedas = 2

    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.iniciar_animacao(
            carregar_frames("atirador", (56, 148), cor=(200, 120, 255)), intervalo=7
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(0, 0, 44, 95)
        self.hitbox.center = self.rect.center
        self.vida_maxima = 2
        self.vida = self.vida_maxima

        self.alvo = None
        self.grupos_tiro = ()          # (todos, bolas) definido pelo gerenciador
        self.y_parada = random.randint(TOPO_HUD + 90, 330)
        self.estado = "descendo"
        self.contador = 0
        self.dir_x = random.choice([-1, 1])

    def _atirar(self):
        if self.alvo is None or not self.grupos_tiro:
            return
        bola = BolaInimiga(
            self.rect.centerx, self.rect.centery + 20,
            self.alvo.rect.centerx, self.alvo.rect.centery
        )
        for grupo in self.grupos_tiro:
            grupo.add(bola)

    def update(self):
        self.animar()
        if self.estado == "descendo":
            self.rect.y += self.velocidade
            if self.rect.centery >= self.y_parada:
                self.estado = "atirando"
        elif self.estado == "atirando":
            self.contador += 1
            self.rect.x += self.dir_x * 2
            if self.rect.left <= 0 or self.rect.right >= LARGURA:
                self.dir_x *= -1
            if self.contador % 75 == 0:
                self._atirar()
            if self.contador >= 420:
                self.estado = "fugindo"
        else:
            self.rect.y += 7

        self.hitbox.center = self.rect.center
        if self.rect.y > ALTURA:
            self.kill()
