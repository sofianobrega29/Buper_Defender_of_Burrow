import pygame
import random
from constantes import *
from classes import *

pygame.init()


TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Buper Defender Of The Burrow")

FPS = 60
clock = pygame.time.Clock()

todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()

jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

pontos = 0
spawn_timer = 0

wave = 0

rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                todos_sprites.add(tiro)
                tiros.add(tiro)

    # timer de entrada dos inimigos
    spawn_timer += 0.5
    if spawn_timer > 60:
        '''inimigo1 = InimigoZigueZague(random.randint(random.randint(1, 40), LARGURA - random.randint(1, 40)), -20)
        inimigo1.direcao *= random.randint(-3, -1)''' '''Inimigo em desenvolvimento'''

        inimigo2 = InimigoPadrao(random.randint(random.randint(1, 40), LARGURA - random.randint(1, 40)), -20)
        todos_sprites.add(inimigo2)
        inimigos.add(inimigo2)
        spawn_timer = 0
        
    # Sistema de Waves (O código abaixo é só um teste)
    if jogador.eliminacoes == 0:
        wave = 1
        
    

    # colisão tiro x robô
    colisao = pygame.sprite.groupcollide(inimigos, tiros, True, True)
    pontos += len(colisao)
    jogador.eliminacoes +=1

    # colisão robô x jogador
    if pygame.sprite.spritecollide(jogador, inimigos, True):
        jogador.vida -= 1
        if jogador.vida <= 0:
            print("GAME OVER!")
            rodando = False

    # atualizar
    todos_sprites.update()

    # desenhar
    BG = pygame.image.load("sprites/background/campo.png")
    BG = pygame.transform.scale(BG, (10, 750))
    TELA.fill((25, 25, 25))
    todos_sprites.draw(TELA)

    #Painel de pontos e vida
    font = pygame.font.SysFont("impact", 30)
    info_player = font.render(f"Vidas: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
    info_wave = font.render(f"Wave: {wave}", True, (255, 255, 255))
    TELA.blit(info_player, (10, 10))
    TELA.blit(info_wave, (650, 10))

    pygame.display.flip()

pygame.quit()