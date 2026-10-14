import os

LARGURA = 800
ALTURA = 1000

VELOCIDADE_JOGADOR = 5

# Altura da barra do HUD (o jogador e as raposas nao entram nela)
TOPO_HUD = 65

# pasta onde esta o jogo.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# arquivo onde o recorde de pontos fica salvo
ARQUIVO_RECORDE = os.path.join(BASE_DIR, "recorde.txt")
