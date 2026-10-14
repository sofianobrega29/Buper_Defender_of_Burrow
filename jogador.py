import pygame
from inimigos.robo import Entidade
from constantes import BASE_DIR, LARGURA, ALTURA, TOPO_HUD
import os


class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        imagem = pygame.image.load(
            os.path.join(BASE_DIR, "sprites", "jogador", "buper.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(imagem, (80, 95))
        self.imagem_original = self.image.copy()
        # Versao branca (piscar ao levar dano). BLEND_RGB_MAX nao mexe no alpha,
        # entao a parte transparente continua transparente.
        self.imagem_branca = self.image.copy()
        self.imagem_branca.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGB_MAX)
        self.tempo_invulneravel = 0
        self.duracao_invulnerabilidade = 1000
        self.intervalo_piscar = 80
        self.rect = self.image.get_rect(center=(x, y))

        self.vida_maxima = 5
        self.vida = self.vida_maxima
        self.eliminacoes = 0

    def receber_dano(self):
        agora = pygame.time.get_ticks()

        if agora < self.tempo_invulneravel:
            return False

        self.vida -= 1
        self.tempo_invulneravel = agora + self.duracao_invulnerabilidade
        return True

    def update(self):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.velocidade
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.velocidade
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.velocidade
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.velocidade

        self.mover(dx, dy)

        agora = pygame.time.get_ticks()

        if agora < self.tempo_invulneravel:
            if (agora // self.intervalo_piscar) % 2 == 0:
                self.image = self.imagem_branca
            else:
                self.image = self.imagem_original
        else:
            self.image = self.imagem_original

        # Mantem o personagem dentro da tela (abaixo do HUD).
        limites = pygame.Rect(0, TOPO_HUD, LARGURA, ALTURA - TOPO_HUD)
        self.rect.clamp_ip(limites)
