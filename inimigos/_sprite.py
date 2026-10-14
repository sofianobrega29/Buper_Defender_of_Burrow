"""Carregamento e animacao dos sprites dos inimigos.

Para cada inimigo existe um NOME (padrao, veloz, ziguezague, tanque, atirador,
investida, raposa, chefe, rei). O jogo procura a arte nesta ordem:

  1. sprites/inimigo/<nome>_1.png, <nome>_2.png ... (ate _8)  -> frames soltos
  2. sprites/inimigo/<nome>_sheet.png                         -> 4 frames lado a lado
  3. nada encontrado -> usa inimigo1.png (tingido) com uma animacao de
     corrida simulada (balanco, inclinacao e espelhamento).

Assim o jogo funciona agora e melhora sozinho quando as imagens novas forem
colocadas na pasta, sem mexer no codigo.
"""
import os
import pygame
from constantes import BASE_DIR

PASTA = os.path.join(BASE_DIR, "sprites", "inimigo")
_CACHE = {}


def _ajustar(imagem, tamanho):
    """Redimensiona mantendo a proporcao e centraliza num quadro fixo."""
    w, h = imagem.get_size()
    esc = min(tamanho[0] / w, tamanho[1] / h)
    novo = pygame.transform.smoothscale(imagem, (max(1, int(w * esc)), max(1, int(h * esc))))
    quadro = pygame.Surface(tamanho, pygame.SRCALPHA)
    quadro.blit(novo, novo.get_rect(center=(tamanho[0] // 2, tamanho[1] // 2)))
    return quadro


def _tingir(imagem, cor):
    imagem = imagem.copy()
    imagem.fill((*cor, 255), special_flags=pygame.BLEND_RGB_MULT)
    return imagem


def _frames_customizados(nome, tamanho):
    frames = []
    for i in range(1, 9):
        caminho = os.path.join(PASTA, f"{nome}_{i}.png")
        if not os.path.exists(caminho):
            break
        frames.append(_ajustar(pygame.image.load(caminho).convert_alpha(), tamanho))
    if frames:
        return frames

    caminho = os.path.join(PASTA, f"{nome}_sheet.png")
    if os.path.exists(caminho):
        folha = pygame.image.load(caminho).convert_alpha()
        largura = folha.get_width() // 4
        return [
            _ajustar(folha.subsurface((i * largura, 0, largura, folha.get_height())).copy(), tamanho)
            for i in range(4)
        ]
    return None


def _frames_simulados(tamanho):
    """Ciclo de corrida falso a partir de uma unica imagem (4 frames)."""
    base = pygame.image.load(os.path.join(PASTA, "inimigo1.png")).convert_alpha()
    base = _ajustar(base, tamanho)
    espelho = pygame.transform.flip(base, True, False)
    w, h = tamanho

    def variar(img, escala_y, graus):
        # estica/achata no eixo vertical (passada) e inclina um pouco
        alt = max(1, int(h * escala_y))
        img = pygame.transform.smoothscale(img, (w, alt))
        img = pygame.transform.rotate(img, graus)
        quadro = pygame.Surface(tamanho, pygame.SRCALPHA)
        quadro.blit(img, img.get_rect(center=(w // 2, h // 2)))
        return quadro

    return [
        variar(base, 1.00, -5),
        variar(espelho, 0.93, 0),
        variar(base, 1.00, 5),
        variar(espelho, 0.93, 0),
    ]


def carregar_frames(nome, tamanho, cor=None, sobreposicao=None, alternativo=None):
    """Devolve a lista de frames do inimigo `nome` no `tamanho` pedido.

    `alternativo` e o nome de outra arte a usar se `nome` nao existir.
    `cor` (tingimento) e `sobreposicao` (RGBA somado) so valem para o
    visual simulado; arte customizada ja vem colorida.
    """
    chave = (nome, tamanho, cor, sobreposicao, alternativo)
    if chave in _CACHE:
        return _CACHE[chave]

    frames = _frames_customizados(nome, tamanho)
    if frames is None and alternativo:
        frames = _frames_customizados(alternativo, tamanho)
    if frames is None:
        frames = _frames_simulados(tamanho)
        if cor is not None:
            frames = [_tingir(f, cor) for f in frames]
        if sobreposicao is not None:
            novos = []
            for f in frames:
                f = f.copy()
                # RGB_ADD so soma cor: nao altera a transparencia (antes o
                # BLEND_RGBA_ADD pintava um retangulo em volta do sprite).
                r, g, b, a = sobreposicao
                f.fill((r * a // 255, g * a // 255, b * a // 255, 0),
                       special_flags=pygame.BLEND_RGB_ADD)
                novos.append(f)
            frames = novos

    _CACHE[chave] = frames
    return frames


def tingir_frames(frames, cor):
    return [_tingir(f, cor) for f in frames]


class Animado:
    """Mistura (mixin) que da animacao por frames a um Sprite."""

    def iniciar_animacao(self, frames, intervalo=6):
        self.frames = frames
        self.intervalo_anim = intervalo
        self.cont_anim = 0
        self.image = frames[0]

    def animar(self):
        self.cont_anim += 1
        self.image = self.frames[(self.cont_anim // self.intervalo_anim) % len(self.frames)]
