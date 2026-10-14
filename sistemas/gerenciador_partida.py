import pygame
from constantes import LARGURA, ALTURA
from map import Mapa
from jogador import Jogador
from sistemas.hud import HUD
from sistemas.gerenciador_ondas import GerenciadorOndas

class GerenciadorPartida:
    def __init__(self):
        self.todos = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.bolas = pygame.sprite.Group()  # tiros dos inimigos
        self.jogador = Jogador(LARGURA // 2, ALTURA - 75)
        self.todos.add(self.jogador)
        self.mapa = Mapa()
        self.hud = HUD(max_waves=10)
        self.ondas = GerenciadorOndas(self.todos, self.inimigos, self.jogador, self.bolas)
        self.pontos = 0
        self.cont_tiro = 0
        self.pausado = False
        self.flash_ate = 0

    @property
    def wave(self):
        return self.ondas.wave