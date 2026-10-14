import pygame
from tiros import Tiro

class GerenciadorTiros:
    def __init__(self, todos, tiros, jogador, tocar_som):
        self.todos = todos
        self.tiros = tiros
        self.jogador = jogador
        self.tocar_som = tocar_som

        self.contador = 0
        self.intervalo = 12

        self.armas = [
            {
                "nome": "Estilingue",
                "dano": 1,
                "preco": 0,
                "cor": (255, 255, 255),
            },
            {
                "nome": "Tiro Azul",
                "dano": 2,
                "preco": 10,
                "cor": (70, 180, 255),
            },
            {
                "nome": "Tiro Dourado",
                "dano": 4,
                "preco": 25,
                "cor": (255, 205, 55),
            },
            {
                "nome": "Tiro Vermelho",
                "dano": 7,
                "preco": 50,
                "cor": (255, 80, 80),
            },
        ]

        self.armas_compradas = {0}
        self.indice_arma = 0

    @property
    def arma_atual(self):
        return self.armas[self.indice_arma]

    def comprar(self, indice, moedas):
        if indice < 0 or indice >= len(self.armas):
            return moedas, False

        arma = self.armas[indice]

        if indice in self.armas_compradas:
            return moedas, False

        if moedas < arma["preco"]:
            return moedas, False

        moedas -= arma["preco"]
        self.armas_compradas.add(indice)
        self.indice_arma = indice

        return moedas, True

    def equipar(self, indice):
        """Equipa uma arma ja comprada. Retorna True se equipou."""
        if indice in self.armas_compradas:
            self.indice_arma = indice
            return True
        return False

    def atualizar(self):
        self.contador += 1
        teclas = pygame.key.get_pressed()

        if (
            teclas[pygame.K_SPACE]
            and self.contador >= self.intervalo
        ):
            arma = self.arma_atual

            tiro = Tiro(
                self.jogador.rect.centerx,
                self.jogador.rect.top,
                dano=arma["dano"],
                cor=arma["cor"],
            )

            self.todos.add(tiro)
            self.tiros.add(tiro)
            self.tocar_som()
            self.contador = 0
