import pygame
from constantes import LARGURA, ALTURA
from .robo import Robo
from ._sprite import Animado, carregar_frames, tingir_frames


class InimigoInvestida(Animado, Robo):
    """Desce devagar, pisca em vermelho (aviso) e mergulha na direcao do jogador."""
    valor_pontos = 30
    valor_moedas = 2

    def __init__(self, x, y):
        super().__init__(x, y, velocidade=4)
        self.frames_normal = carregar_frames("investida", (58, 142), cor=(255, 150, 150))
        # no aviso/mergulho o inimigo fica avermelhado
        self.frames_alerta = tingir_frames(self.frames_normal, (255, 90, 90))
        self.iniciar_animacao(self.frames_normal, intervalo=5)
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(0, 0, 46, 95)
        self.hitbox.center = self.rect.center
        self.pos_x, self.pos_y = float(self.rect.x), float(self.rect.y)
        self.alvo = None
        self.estado = "descendo"
        self.contador = 0
        self.vx = self.vy = 0.0
        self.y_alerta = 260

    def update(self):
        self.animar()
        if self.estado == "descendo":
            self.pos_y += self.velocidade
            if self.pos_y >= self.y_alerta:
                self.estado = "alerta"
        elif self.estado == "alerta":
            self.contador += 1
            self.frames = self.frames_alerta if (self.contador // 5) % 2 == 0 else self.frames_normal
            if self.contador >= 40:
                self.estado = "investindo"
                self.frames = self.frames_alerta
                self.intervalo_anim = 3
                if self.alvo is not None:
                    dx = self.alvo.rect.centerx - self.rect.centerx
                    dy = self.alvo.rect.centery - self.rect.centery
                else:
                    dx, dy = 0, 1
                dist = max(1, (dx * dx + dy * dy) ** 0.5)
                self.vx, self.vy = dx / dist * 13, dy / dist * 13
        else:
            self.pos_x += self.vx
            self.pos_y += self.vy

        self.rect.x, self.rect.y = round(self.pos_x), round(self.pos_y)
        self.hitbox.center = self.rect.center
        if (
            self.rect.top > ALTURA or self.rect.right < -50
            or self.rect.left > LARGURA + 50
        ):
            self.kill()
