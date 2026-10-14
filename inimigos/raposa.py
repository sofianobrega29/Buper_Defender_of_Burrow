import pygame
from constantes import LARGURA, TOPO_HUD
from ._sprite import Animado, carregar_frames


class Raposa(Animado, pygame.sprite.Sprite):
    """Raposa normal (3 de vida) ou chefe gigante. Persegue o jogador.

    `nome_sprite` escolhe a arte: "raposa", "chefe" (onda 5) ou "rei" (onda 10).
    """
    def __init__(self, x, y, gigante=False, vida_chefe=120, nome_sprite=None):
        super().__init__()
        self.gigante = gigante
        nome = nome_sprite or ("chefe" if gigante else "raposa")
        tamanho = {"chefe": (100, 300), "rei": (150, 300)}.get(nome, (56, 170))
        # sem arte propria, fica laranja (visual simulado)
        self.iniciar_animacao(
            carregar_frames(
                nome, tamanho,
                alternativo="chefe",  # raposa comum usa a arte do chefe em tamanho menor
                sobreposicao=(
                    (190, 40, 220, 110) if nome == "rei"
                    else (255, 105, 20, 105 if gigante else 70)
                ),
            ),
            intervalo=8 if gigante else 5,
        )
        self.rect = self.image.get_rect(center=(x, y))
        # Posicao em float: antes o round() deixava o movimento torto/travado
        # (a raposa gigante, de velocidade 1.45, quase nao andava na diagonal).
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.velocidade = 1.45 if gigante else 2.3
        self.alvo = None
        self.vida_maxima = vida_chefe if gigante else 3
        self.vida = self.vida_maxima
        self.valor_moedas = 10 if gigante else 3
        self.valor_pontos = 200 if gigante else 30
        self.hitbox = self.rect.inflate(-20, -25)

    def update(self):
        self.animar()
        if self.alvo is None or not self.alvo.alive():
            return

        # Entra na tela vindo de cima antes de comecar a perseguir.
        if self.rect.top < TOPO_HUD:
            self.pos_y += 2
        else:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = max(1, (dx * dx + dy * dy) ** 0.5)
            self.pos_x += dx / distancia * self.velocidade
            self.pos_y += dy / distancia * self.velocidade

        self.rect.x = round(self.pos_x)
        self.rect.y = round(self.pos_y)
        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))
        self.pos_x = float(self.rect.x)
        self.hitbox.center = self.rect.center
