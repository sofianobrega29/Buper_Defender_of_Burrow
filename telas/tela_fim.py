import pygame

class TelaFim:
    def __init__(self,tela,clock,fps,largura,altura,fonte,fonte_titulo,fonte_pequena):
        self.tela = tela
        self.clock = clock
        self.fps = fps
        self.largura = largura
        self.altura = altura

        self.fonte = fonte
        self.fonte_titulo = fonte_titulo
        self.fonte_pequena = fonte_pequena

        self.opcoes = ["JOGAR NOVAMENTE", "MENU PRINCIPAL", "SAIR"]

    def _texto_central(self, texto, fonte, cor, y):
        imagem = fonte.render(texto, True, cor)
        x = self.largura // 2 - imagem.get_width() // 2
        self.tela.blit(imagem, (x, y))

    def _desenhar_botao(self, texto, y, selecionado=False):
        cor = (255, 230, 120) if selecionado else (255, 255, 255)
        imagem = self.fonte.render(texto, True, cor)
        caixa = imagem.get_rect(center=(self.largura // 2, y))

        fundo = caixa.inflate(44, 28)

        pygame.draw.rect(self.tela,(25, 45, 27),fundo,border_radius=8)
        pygame.draw.rect(self.tela,cor,fundo,2,border_radius=8)

        self.tela.blit(imagem, caixa)
        return fundo

    def executar(self, pontos, wave, vitoria=False, recorde=0, novo_recorde=False):
        selecionado = 0
        caixas = []

        resultados = ["jogar", "menu", "sair"]

        while True:
            self.clock.tick(self.fps)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"

                if evento.type == pygame.KEYDOWN:
                    if evento.key in (pygame.K_UP, pygame.K_w):
                        selecionado = (selecionado - 1) % len(self.opcoes)

                    elif evento.key in (pygame.K_DOWN, pygame.K_s):
                        selecionado = (selecionado + 1) % len(self.opcoes)

                    elif evento.key in (pygame.K_RETURN,pygame.K_SPACE):
                        return resultados[selecionado]

                elif (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                    for indice, caixa in enumerate(caixas):
                        if caixa.collidepoint(evento.pos):
                            return resultados[indice]

            self.tela.fill((15, 28, 19))

            titulo = "VITORIA!" if vitoria else "FIM DE JOGO"
            cor_titulo = (255, 226, 110) if vitoria else (255, 105, 105)
            self._texto_central(titulo,self.fonte_titulo,cor_titulo,250)
            self._texto_central(f"PONTUACAO: {pontos}",self.fonte,(255, 255, 255),370)
            self._texto_central(f"ONDA ALCANCADA: {wave}",self.fonte_pequena,(255, 226, 110),420)
            if novo_recorde:
                self._texto_central("NOVO RECORDE!",self.fonte_pequena,(120, 255, 140),460)
            else:
                self._texto_central(f"RECORDE: {recorde}",self.fonte_pequena,(190, 220, 190),460)

            caixas = []

            for indice, opcao in enumerate(self.opcoes):
                caixas.append(self._desenhar_botao(opcao,535 + indice * 85,indice == selecionado))

            pygame.display.flip()