import pygame
from constantes import *
import os

class Mapa:
    def __init__(self):
        caminho_mapa = (os.path.join(BASE_DIR, "sprites", "background", "campo.png"))
        self.imagem = pygame.image.load(caminho_mapa).convert()

        self.imagem = pygame.transform.scale(
            self.imagem, (LARGURA, ALTURA)
        )

    def desenhar(self, tela):
        tela.blit(self.imagem, (0, 0))