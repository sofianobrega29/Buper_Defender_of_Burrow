import os
import pygame
from constantes import BASE_DIR

class Recursos:
    def __init__(self):
        self.audio_disponivel = False

        try:
            pygame.mixer.init()
            self.audio_disponivel = True
        except pygame.error:
            pass

    def caminho(self, *partes):
        return os.path.join(BASE_DIR, *partes)

    def carregar_fonte(self, nome, tamanho):
        try:
            return pygame.font.Font(
                self.caminho("sprites", "fontes", nome),
                tamanho
            )
        except (pygame.error, OSError):
            return pygame.font.Font(None, tamanho)

    def carregar_som(self, nome):
        if not self.audio_disponivel:
            return None

        try:
            som = pygame.mixer.Sound(
                self.caminho("sons", nome)
            )
            som.set_volume(0.45)
            return som
        except (pygame.error, OSError):
            return None

    def tocar(self, som):
        if som is not None:
            try:
                som.play()
            except pygame.error:
                pass

    def iniciar_musica(self, nome, volume=0.25):
        if not self.audio_disponivel:
            return

        try:
            pygame.mixer.music.load(self.caminho("sons", nome))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except (pygame.error, OSError):
            pass
