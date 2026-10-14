import os
import pygame
from constantes import LARGURA, ALTURA, BASE_DIR, TOPO_HUD

COR_ARMAS = {
    "Estilingue": (255, 255, 255),
    "Tiro Azul": (70, 180, 255),
    "Tiro Dourado": (255, 205, 55),
    "Tiro Vermelho": (255, 80, 80),
}


class HUD:
    def __init__(self, max_waves=5):
        self.max_waves = max_waves
        self.fonte = pygame.font.Font(None, 28)
        self.fonte_grande = pygame.font.Font(None, 38)
        self.fonte_pequena = pygame.font.Font(None, 20)
        self.coracao_cheio = None
        self.coracao_vazio = None
        self.icone_moeda = None
        self.icones_arma = {}
        self._carregar_sprites()

    def _carregar_sprites(self):
        """Carrega os desenhos usados no HUD (coracoes, moeda, tiros)."""
        try:
            folha = pygame.image.load(
                os.path.join(BASE_DIR, "assets", "sprites", "coracao.png")
            ).convert_alpha()
            cheio = folha.subsurface((65, 60, 200, 170)).copy()
            vazio = folha.subsurface((755, 285, 205, 170)).copy()
            self.coracao_cheio = pygame.transform.smoothscale(cheio, (28, 24))
            self.coracao_vazio = pygame.transform.smoothscale(vazio, (28, 24))
        except (pygame.error, OSError, ValueError):
            pass

        try:
            moeda = pygame.image.load(
                os.path.join(BASE_DIR, "assets", "sprites", "moeda.png")
            ).convert_alpha()
            self.icone_moeda = pygame.transform.smoothscale(moeda, (26, 26))
        except (pygame.error, OSError):
            self.icone_moeda = pygame.Surface((26, 26), pygame.SRCALPHA)
            pygame.draw.circle(self.icone_moeda, (255, 210, 45), (13, 13), 12)

        try:
            tiro = pygame.image.load(
                os.path.join(BASE_DIR, "sprites", "jogador", "tiro.png")
            ).convert_alpha()
            tiro = pygame.transform.smoothscale(tiro, (16, 32))
            for nome, cor in COR_ARMAS.items():
                icone = tiro.copy()
                if cor != (255, 255, 255):
                    icone.fill((*cor, 255), special_flags=pygame.BLEND_RGB_MULT)
                self.icones_arma[nome] = icone
        except (pygame.error, OSError):
            pass

    def _caixa(self, tela, rect, cor_borda=(90, 150, 100)):
        pygame.draw.rect(tela, (32, 46, 38), rect, border_radius=8)
        pygame.draw.rect(tela, cor_borda, rect, 2, border_radius=8)

    def desenhar(
        self,
        tela,
        jogador,
        pontos,
        wave,
        moedas=0,
        arma_nome="Estilingue",
        chefe=None
    ):
        # Fundo e friso da barra superior
        pygame.draw.rect(tela, (20, 28, 24), (0, 0, LARGURA, TOPO_HUD))
        pygame.draw.line(tela, (90, 150, 100), (0, TOPO_HUD - 1), (LARGURA, TOPO_HUD - 1), 2)

        # --- Vida (coracoes) ---
        vida = max(0, jogador.vida)
        if self.coracao_cheio is not None:
            for i in range(jogador.vida_maxima):
                imagem = self.coracao_cheio if i < vida else self.coracao_vazio
                tela.blit(imagem, (12 + i * 31, 6))
        else:
            texto_vida = self.fonte.render(f"VIDA: {vida}", True, (255, 100, 100))
            tela.blit(texto_vida, (12, 8))

        # --- Moedas (icone + valor) ---
        tela.blit(self.icone_moeda, (12, 34))
        texto_moedas = self.fonte.render(f"x {moedas}", True, (255, 220, 80))
        tela.blit(texto_moedas, (44, 38))

        # --- Pontos (caixa central) ---
        caixa_pontos = pygame.Rect(0, 0, 190, 50)
        caixa_pontos.center = (LARGURA // 2 - 70, TOPO_HUD // 2)
        self._caixa(tela, caixa_pontos)
        rotulo = self.fonte_pequena.render("PONTOS", True, (150, 190, 155))
        tela.blit(rotulo, (caixa_pontos.centerx - rotulo.get_width() // 2, caixa_pontos.y + 5))
        valor = self.fonte_grande.render(str(pontos), True, (255, 255, 255))
        tela.blit(valor, (caixa_pontos.centerx - valor.get_width() // 2, caixa_pontos.y + 20))

        # --- Arma equipada (slot com o icone do tiro) ---
        slot = pygame.Rect(0, 0, 190, 50)
        slot.center = (LARGURA // 2 + 122, TOPO_HUD // 2)
        cor_arma = COR_ARMAS.get(arma_nome, (255, 255, 255))
        self._caixa(tela, slot, cor_borda=cor_arma)
        icone = self.icones_arma.get(arma_nome)
        if icone is not None:
            tela.blit(icone, (slot.x + 12, slot.centery - icone.get_height() // 2))
        rotulo = self.fonte_pequena.render("ARMA", True, (150, 190, 155))
        tela.blit(rotulo, (slot.x + 40, slot.y + 6))
        nome = self.fonte.render(arma_nome, True, cor_arma)
        tela.blit(nome, (slot.x + 40, slot.y + 22))

        # --- Onda (rotulo + bolinhas de progresso) ---
        texto_onda = self.fonte.render(f"ONDA {wave}/{self.max_waves}", True, (255, 225, 110))
        x_onda = LARGURA - texto_onda.get_width() - 14
        tela.blit(texto_onda, (x_onda, 8))
        # barra de progresso das ondas
        barra = pygame.Rect(LARGURA - 14 - 80, 34, 80, 10)
        pygame.draw.rect(tela, (70, 80, 70), barra, border_radius=4)
        preenchido = barra.copy()
        preenchido.width = int(barra.width * min(wave, self.max_waves) / self.max_waves)
        pygame.draw.rect(tela, (255, 225, 110), preenchido, border_radius=4)
        pygame.draw.rect(tela, (150, 190, 155), barra, 1, border_radius=4)

        # --- Tecla da loja desenhada como "keycap" ---
        tecla = pygame.Rect(628, 28, 24, 22)
        pygame.draw.rect(tela, (60, 60, 50), tecla, border_radius=5)
        pygame.draw.rect(tela, (255, 220, 100), tecla, 2, border_radius=5)
        letra = self.fonte_pequena.render("B", True, (255, 220, 100))
        tela.blit(letra, (tecla.centerx - letra.get_width() // 2, tecla.centery - letra.get_height() // 2))
        loja = self.fonte_pequena.render("LOJA", True, (255, 220, 100))
        tela.blit(loja, (tecla.right + 6, tecla.centery - loja.get_height() // 2))

        # --- Vida do chefe ---
        if (
            chefe is not None
            and chefe.alive()
            and getattr(chefe, "gigante", False)
        ):
            vida_maxima = max(1, chefe.vida_maxima)
            proporcao = max(0, min(1, chefe.vida / vida_maxima))

            largura = min(360, LARGURA - 40)
            x = (LARGURA - largura) // 2
            y = TOPO_HUD + 13

            pygame.draw.rect(tela, (45, 25, 25), (x, y, largura, 16))
            pygame.draw.rect(tela, (220, 55, 45), (x, y, int(largura * proporcao), 16))
            pygame.draw.rect(tela, (255, 255, 255), (x, y, largura, 16), 2)

            texto_chefe = self.fonte_pequena.render(
                f"RAPOSA GIGANTE: {max(0, chefe.vida)}/{vida_maxima}",
                True, (255, 240, 230)
            )
            tela.blit(
                texto_chefe,
                (LARGURA // 2 - texto_chefe.get_width() // 2, y + 19)
            )

    def animar_dano(self, vida_atual):
        pass
