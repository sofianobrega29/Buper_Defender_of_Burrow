import pygame
from constantes import LARGURA, ALTURA, BASE_DIR
from sistemas.recursos import Recursos
from sistemas.gerenciador_partida import GerenciadorPartida
from sistemas.gerenciador_tiros import GerenciadorTiros
from sistemas.colisoes import GerenciadorColisoes
from inimigos.raposa import Raposa
from telas.tela_fim import TelaFim
from telas.tela_menu import TelaMenu
from sistemas.recorde import carregar_recorde, salvar_recorde

pygame.init()
recursos = Recursos()
def criar_janela():
    """Cria a janela e devolve a superficie onde o jogo desenha (800x1000).

    Se a tela do computador for menor que o jogo (ex.: notebook com 768px de
    altura), a janela e reduzida e o desenho e escalado a cada frame. Antes o
    topo da janela ficava fora da tela, escondendo o HUD.
    """
    info = pygame.display.Info()
    escala = min(
        1.0,
        (info.current_h - 110) / ALTURA,
        (info.current_w - 20) / LARGURA,
    )
    if escala <= 0 or info.current_h <= 0:
        escala = 1.0

    if escala >= 0.999:
        return pygame.display.set_mode((LARGURA, ALTURA)), 1.0

    tamanho = (int(LARGURA * escala), int(ALTURA * escala))
    janela = pygame.display.set_mode(tamanho)
    virtual = pygame.Surface((LARGURA, ALTURA))

    flip_original = pygame.display.flip
    event_get_original = pygame.event.get

    def flip():
        pygame.transform.smoothscale(virtual, tamanho, janela)
        flip_original()

    def event_get(*args, **kwargs):
        eventos = event_get_original(*args, **kwargs)
        for e in eventos:
            if hasattr(e, "pos"):
                # converte o clique da janela para as coordenadas do jogo
                e.pos = (int(e.pos[0] / escala), int(e.pos[1] / escala))
        return eventos

    pygame.display.flip = flip
    pygame.event.get = event_get
    return virtual, escala


TELA, ESCALA_JANELA = criar_janela()
pygame.display.set_caption("Buper: Defender of Burrow")
CLOCK = pygame.time.Clock()
FPS = 60

FONTE_TITULO = recursos.carregar_fonte("PressStart2P.ttf", 30)
FONTE = recursos.carregar_fonte("PressStart2P.ttf", 16)
FONTE_PEQUENA = recursos.carregar_fonte("PressStart2P.ttf", 11)
som_tiro = recursos.carregar_som("estilingue_tiro.mp3")
som_colisao = recursos.carregar_som("Cachorro.mp3")
recursos.iniciar_musica("trilha_sonora2.ogg")


def texto_central(texto, fonte, cor, y, superficie=TELA):
    imagem = fonte.render(texto, True, cor)
    x = superficie.get_width() // 2 - imagem.get_width() // 2
    superficie.blit(imagem, (x, y))


def desenhar_loja(moedas, gerenciador_tiros, mensagem=""):
    sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 205))
    TELA.blit(sombra, (0, 0))

    painel = pygame.Rect(95, 170, LARGURA - 190, 660)
    pygame.draw.rect(TELA, (22, 42, 29), painel, border_radius=12)
    pygame.draw.rect(TELA, (255, 220, 90), painel, 3, border_radius=12)

    texto_central("LOJA DE TIROS", FONTE_TITULO, (255, 226, 110), 205)
    texto_central(f"MOEDAS DISPONIVEIS: {moedas}", FONTE, (255, 230, 110), 270)
    texto_central(
        f"TIRO EQUIPADO: {gerenciador_tiros.arma_atual['nome']}",
        FONTE_PEQUENA, (150, 220, 255), 315
    )

    linhas = [
        "1 - ESTILINGUE BASICO | DANO 1 | GRATIS",
        "2 - TIRO AZUL | DANO 2 | 10 MOEDAS",
        "3 - TIRO DOURADO | DANO 4 | 25 MOEDAS",
        "4 - TIRO VERMELHO | DANO 7 | 50 MOEDAS",
        "5 - CURA +1 VIDA | 15 MOEDAS",
        "",
        "APERTE O NUMERO PARA COMPRAR OU EQUIPAR.",
        "AS MELHORIAS PERMANECEM ATE O FIM DA PARTIDA.",
        "B OU ESC PARA VOLTAR",
    ]

    for i, linha in enumerate(linhas):
        texto_central(linha, FONTE_PEQUENA, (245, 245, 245), 375 + i * 36)

    if mensagem:
        texto_central(mensagem, FONTE_PEQUENA, (255, 180, 120), ALTURA - 35)


TECLAS_ARMAS = {
    pygame.K_2: 1, pygame.K_KP2: 1,
    pygame.K_3: 2, pygame.K_KP3: 2,
    pygame.K_4: 3, pygame.K_KP4: 3,
}
PRECO_CURA = 15


def jogar():
    partida = GerenciadorPartida()
    todos = partida.todos
    inimigos = partida.inimigos
    tiros = partida.tiros
    bolas = partida.bolas
    jogador = partida.jogador
    mapa = partida.mapa
    hud = partida.hud
    gerenciador_ondas = partida.ondas

    gerenciador_tiros = GerenciadorTiros(
        todos, tiros, jogador, lambda: recursos.tocar(som_tiro)
    )

    pontos = 0
    moedas = 0
    moedas_no_chao = pygame.sprite.Group()
    pausado = False
    loja_aberta = False
    flash_ate = 0
    mensagem_loja = ""
    mensagem_loja_ate = 0

    while True:
        CLOCK.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                if loja_aberta:
                    if evento.key in (pygame.K_b, pygame.K_ESCAPE):
                        loja_aberta = False
                    elif evento.key in (pygame.K_1, pygame.K_KP1):
                        gerenciador_tiros.equipar(0)
                        mensagem_loja = "ESTILINGUE EQUIPADO!"
                        mensagem_loja_ate = pygame.time.get_ticks() + 1800
                    elif evento.key in TECLAS_ARMAS:
                        indice = TECLAS_ARMAS[evento.key]
                        nome = gerenciador_tiros.armas[indice]["nome"].upper()
                        if gerenciador_tiros.equipar(indice):
                            mensagem_loja = f"{nome} EQUIPADO!"
                        else:
                            moedas, comprou = gerenciador_tiros.comprar(indice, moedas)
                            mensagem_loja = (
                                f"{nome} COMPRADO E EQUIPADO!" if comprou
                                else "MOEDAS INSUFICIENTES."
                            )
                        mensagem_loja_ate = pygame.time.get_ticks() + 1800
                    elif evento.key in (pygame.K_5, pygame.K_KP5):
                        if jogador.vida >= jogador.vida_maxima:
                            mensagem_loja = "SUA VIDA JA ESTA CHEIA."
                        elif moedas < PRECO_CURA:
                            mensagem_loja = "MOEDAS INSUFICIENTES."
                        else:
                            moedas -= PRECO_CURA
                            jogador.vida += 1
                            mensagem_loja = "+1 VIDA!"
                        mensagem_loja_ate = pygame.time.get_ticks() + 1800
                else:
                    if evento.key == pygame.K_ESCAPE:
                        pausado = not pausado
                    elif evento.key == pygame.K_b and not pausado:
                        loja_aberta = True
                        mensagem_loja = ""
                    elif evento.key == pygame.K_q and pausado:
                        return "menu"

        if loja_aberta:
            mapa.desenhar(TELA)
            todos.draw(TELA)

            chefe = next(
                (
                    inimigo for inimigo in inimigos
                    if isinstance(inimigo, Raposa) and inimigo.gigante
                ),
                None
            )

            hud.desenhar(
                TELA, jogador, pontos, gerenciador_ondas.wave,
                moedas, gerenciador_tiros.arma_atual["nome"], chefe
            )

            mensagem = (
                mensagem_loja
                if pygame.time.get_ticks() < mensagem_loja_ate
                else ""
            )

            desenhar_loja(moedas, gerenciador_tiros, mensagem)
            pygame.display.flip()
            continue

        if pausado:
            mapa.desenhar(TELA)
            todos.draw(TELA)
            hud.desenhar(
                TELA, jogador, pontos, gerenciador_ondas.wave,
                moedas, gerenciador_tiros.arma_atual["nome"]
            )

            camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            camada.fill((0, 0, 0, 175))
            TELA.blit(camada, (0, 0))

            texto_central(
                "JOGO PAUSADO", FONTE_TITULO,
                (255, 226, 110), 390
            )
            texto_central(
                "APERTE ESC PARA CONTINUAR",
                FONTE_PEQUENA, (255, 255, 255), 475
            )
            texto_central(
                "Q PARA SAIR PARA O MENU",
                FONTE_PEQUENA, (200, 200, 200), 520
            )
            pygame.display.flip()
            continue

        gerenciador_tiros.atualizar()
        gerenciador_ondas.atualizar()
        wave = gerenciador_ondas.wave

        derrotados, pontos_ganhos = GerenciadorColisoes.verificar_tiros(
            inimigos, tiros, todos, moedas_no_chao
        )
        pontos += pontos_ganhos
        jogador.eliminacoes += derrotados

        recebeu_dano = GerenciadorColisoes.verificar_jogador(
            jogador, inimigos
        )
        # Bolas do Atirador (ficam em "bolas", nao contam para a onda).
        if GerenciadorColisoes.verificar_bolas(jogador, bolas):
            recebeu_dano = True

        if recebeu_dano:
            recursos.tocar(som_colisao)
            flash_ate = pygame.time.get_ticks() + 110
            hud.animar_dano(jogador.vida)

            if jogador.vida <= 0:
                return "fim", pontos, wave

        todos.update()

        coletadas = pygame.sprite.spritecollide(
            jogador, moedas_no_chao, True
        )
        for moeda in coletadas:
            moedas += moeda.valor

        mapa.desenhar(TELA)

        chefe = next(
            (
                inimigo
                for inimigo in inimigos
                if isinstance(inimigo, Raposa) and inimigo.gigante
            ),
            None
        )
        
        todos.draw(TELA)
        
        hud.desenhar(
            TELA,
            jogador,
            pontos,
            wave,
            moedas,
            gerenciador_tiros.arma_atual["nome"],
            chefe
        )

        if pygame.time.get_ticks() < flash_ate:
            flash = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 115))
            TELA.blit(flash, (0, 0))

        pygame.display.flip()

        if gerenciador_ondas.concluido:
            return "vitoria", pontos, wave


def main():
    menu = TelaMenu(
        TELA, CLOCK, FPS, LARGURA, ALTURA, BASE_DIR,
        FONTE, FONTE_TITULO, FONTE_PEQUENA
    )
    menu.obter_recorde = carregar_recorde
    estado = "menu"

    while estado != "sair":
        if estado == "menu":
            estado = menu.executar_menu()
        elif estado == "instrucoes":
            estado = menu.executar_instrucoes()
        elif estado == "jogar":
            resultado = jogar()

            if resultado == "sair":
                estado = "sair"
            elif resultado == "menu":
                estado = "menu"
            else:
                tipo, pontos, wave = resultado
                novo_recorde = salvar_recorde(pontos)
                tela_fim = TelaFim(
                    TELA, CLOCK, FPS, LARGURA, ALTURA,
                    FONTE, FONTE_TITULO, FONTE_PEQUENA
                )
                estado = tela_fim.executar(
                    pontos, wave, vitoria=(tipo == "vitoria"),
                    recorde=carregar_recorde(), novo_recorde=novo_recorde
                )
        else:
            estado = "menu"

    pygame.quit()


if __name__ == "__main__":
    main()
