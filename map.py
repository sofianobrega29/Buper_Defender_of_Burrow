import os
import pygame
from constantes import BASE_DIR, LARGURA, ALTURA

class Mapa:
    def __init__(self):
        caminho_mapa = os.path.join(BASE_DIR,"sprites","background","campo.png")
        imagem = pygame.image.load(caminho_mapa).convert()

        # Preserva a proporção da imagem, ajustando apenas a largura.
        proporcao = LARGURA / imagem.get_width()
        altura = int(imagem.get_height() * proporcao)

        self.imagem = pygame.transform.scale(imagem, (LARGURA, altura))

        self.altura = self.imagem.get_height()
        self.offset_y = 0
        self.velocidade_rolagem = 2

    def desenhar(self, tela):
        # Move o cenário para cima.
        self.offset_y -= self.velocidade_rolagem

        # Reinicia a posição ao completar a rolagem.
        if self.offset_y <= -self.altura:
            self.offset_y = 0

        # Desenha duas cópias consecutivas do cenário.
        tela.blit(self.imagem, (0, self.offset_y))
        tela.blit(self.imagem, (0, self.offset_y + self.altura))
