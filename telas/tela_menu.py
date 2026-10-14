import os
import pygame

class TelaMenu:
    def __init__(self,tela,clock,fps,largura,altura,base_dir,fonte,fonte_titulo,fonte_pequena):
        self.tela = tela
        self.clock = clock
        self.fps = fps
        self.largura = largura
        self.altura = altura
        self.fonte = fonte
        self.fonte_titulo = fonte_titulo
        self.fonte_pequena = fonte_pequena

        caminho_fundo = os.path.join(base_dir, "sprites", "background", "campo_tela.png")

        try:
            imagem = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(imagem, (largura, altura))
            self.fundo.set_alpha(100)
        except (pygame.error, OSError):
            self.fundo = None

        self.obter_recorde = lambda: 0
        self.sombra = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.sombra.fill((0, 0, 0, 135))

    def _texto_central(self, texto, fonte, cor, y):
        imagem = fonte.render(texto, True, cor)
        x = self.largura // 2 - imagem.get_width() // 2
        self.tela.blit(imagem, (x, y))

    def _desenhar_botao(self, texto, y, selecionado=False):
        cor = (255, 230, 120) if selecionado else (255, 255, 255)
        imagem = self.fonte.render(texto, True, cor)
        caixa = imagem.get_rect(center=(self.largura // 2, y))
        fundo = caixa.inflate(44, 28)

        pygame.draw.rect(
            self.tela, (25, 45, 27), fundo, border_radius=8
        )
        pygame.draw.rect(
            self.tela, cor, fundo, 2, border_radius=8
        )

        self.tela.blit(imagem, caixa)
        return fundo

    def executar_menu(self):
        selecionado = 0
        caixas = []
        opcoes = ["JOGAR", "COMO JOGAR", "SAIR"]
        resultados = ["jogar", "instrucoes", "sair"]

        while True:
            self.clock.tick(self.fps)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"

                if evento.type == pygame.KEYDOWN:
                    if evento.key in (pygame.K_UP, pygame.K_w):
                        selecionado = (selecionado - 1) % len(opcoes)

                    elif evento.key in (pygame.K_DOWN, pygame.K_s):
                        selecionado = (selecionado + 1) % len(opcoes)

                    elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return resultados[selecionado]

                elif (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                    for indice, caixa in enumerate(caixas):
                        if caixa.collidepoint(evento.pos):
                            return resultados[indice]

            self.tela.fill((15, 35, 22))

            if self.fundo is not None:
                self.tela.blit(self.fundo, (0, 0))

            self.tela.blit(self.sombra, (0, 0))

            self._texto_central("BUPER", self.fonte_titulo,(255, 226, 110), 180)
            self._texto_central("DEFENDER OF BURROW", self.fonte_pequena,(255, 255, 255), 255)
            self._texto_central("Proteja o burrow e sobreviva!",self.fonte_pequena, (220, 240, 220), 330)

            self._texto_central(f"RECORDE: {self.obter_recorde()}",self.fonte_pequena,(190, 230, 190),385)

            caixas = []
            for indice, opcao in enumerate(opcoes):
                caixas.append(self._desenhar_botao(opcao, 470 + indice * 85,indice == selecionado))

            self._texto_central("WASD / SETAS: MOVER | ESPACO: ATIRAR",self.fonte_pequena, (235, 235, 235),self.altura - 45)

            pygame.display.flip()

    def executar_instrucoes(self):
        linhas = [
            "MOVA-SE COM WASD OU AS SETAS.",
            "SEGURE ESPACO PARA DISPARAR.",
            "DESTRUA OS INIMIGOS PARA GANHAR PONTOS.",
            "NAO DEIXE OS INIMIGOS ENCOSTAREM EM VOCE.",
            "COLETE AS MOEDAS E APERTE B PARA A LOJA.",
            "ESC PAUSA O JOGO.",
            "SOBREVIVA AS 10 ONDAS E VENCA OS CHEFES!",
            "CUIDADO: ALGUNS INIMIGOS ATIRAM OU INVESTEM!",
            "",
            "APERTE ENTER OU ESC PARA VOLTAR."
        ]

        while True:
            self.clock.tick(self.fps)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"

                if evento.type == pygame.KEYDOWN:
                    if evento.key in (pygame.K_ESCAPE,pygame.K_RETURN,pygame.K_SPACE):
                        return "menu"

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    return "menu"

            self.tela.fill((15, 35, 22))

            self._texto_central("COMO JOGAR", self.fonte_titulo,(255, 226, 110), 200)

            for indice, linha in enumerate(linhas):
                self._texto_central(linha, self.fonte_pequena,(255, 255, 255), 330 + indice * 48)

            pygame.display.flip()
