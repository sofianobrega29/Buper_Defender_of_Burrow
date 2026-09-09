import pygame
import random
from classes import *

pygame.init()

from constantes import *

FONTEINFO = pygame.font.Font(
    "sprites/fontes/PressStart2P.ttf",
    24
)

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Buper Defender Of The Burrow")

FPS = 60
clock = pygame.time.Clock()
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()

jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

BG = pygame.image.load("sprites/background/campo.png")
BG = pygame.transform.scale(BG, (LARGURA, ALTURA + 150))

pontos = 0
spawn_timer = 0

cont_tiro = 0

wave = 1
inimigos_wave = 5
inimigos_spawnados = 0
intervalo_spawn = 90


rodando = True

while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if cont_tiro > 2:
                    tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
                    cont_tiro = 0


    #Aumento de dificuldade (Teste)
    cont_tiro += 0.1
    
    #Aumento de waves (Teste)
    if jogador.eliminacoes == 3:
        pass

    spawn_timer += 1
    #Tempo de spawn dos inimigos (Teste)
    if inimigos_spawnados == inimigos_wave:
        wave += 1
        inimigos_wave += 2
        inimigos_spawnados = 0
        inimigo1.aumentar_velocidade()
        
    if inimigos_spawnados <= inimigos_wave:
        if spawn_timer > intervalo_spawn:
            inimigo1 = InimigoPadrao(random.randint(40, LARGURA - 40), -20)

            todos_sprites.add(inimigo1)
            inimigos.add(inimigo1)
            if wave > 6:
                inimigo2 = InimigoZigueZague(random.randint(40, LARGURA - 40), -20)

                todos_sprites.add(inimigo2)
                inimigos.add(inimigo2)

            if wave > 4:
                inimigo3 = InimigoVeloz(random.randint(40, LARGURA - 40), -20)
                
                todos_sprites.add(inimigo3)
                inimigos.add(inimigo3)

            spawn_timer = 0
            inimigos_spawnados += 1

    #Colisão dos tiros com os inimigos
    colisao = pygame.sprite.groupcollide(inimigos, tiros, True, True)

    pontos += len(colisao)
    jogador.eliminacoes += len(colisao)

    #Colisão do Buper e os inimigos
    if pygame.sprite.spritecollide(jogador, inimigos, True):
        jogador.vida -= 1

        if jogador.vida <= 0:
            print("GAME OVER!")
            rodando = False

    todos_sprites.update()

    #Desenho e info do player
    TELA.fill((0, 0, 0))
    todos_sprites.draw(TELA)

    info_player = FONTEINFO.render(f"Vidas: {jogador.vida} | Pontos: {pontos}", True, (255, 255, 255))

    info_wave = FONTEINFO.render(f"Wave: {wave}", True, (255, 255, 255))

    TELA.blit(info_player, (10, 10))
    TELA.blit(info_wave, (620, 10))

    pygame.display.flip()

pygame.quit()
