from inimigos.raposa import Raposa
from sistemas.moeda import Moeda


class GerenciadorColisoes:
    @staticmethod
    def verificar_tiros(inimigos, tiros, todos, moedas_no_chao):
        """Retorna (inimigos derrotados, pontos ganhos)."""
        derrotados = 0
        pontos = 0

        for tiro in list(tiros):
            if not tiro.alive():
                continue

            for inimigo in list(inimigos):
                if not inimigo.alive():
                    continue

                hitbox = getattr(inimigo, "hitbox", inimigo.rect)

                if not tiro.rect.colliderect(hitbox):
                    continue

                dano = getattr(tiro, "dano", 1)

                # Inimigos com "vida" (raposas, tanque, atirador) aguentam mais de um tiro.
                if hasattr(inimigo, "vida"):
                    inimigo.vida -= dano

                    if inimigo.vida > 0:
                        tiro.kill()
                        break

                # Guarda a posicao e a recompensa antes de remover o inimigo.
                x, y = inimigo.rect.center
                valor = getattr(inimigo, "valor_moedas", 1)

                inimigo.kill()
                derrotados += 1
                pontos += getattr(inimigo, "valor_pontos", 10)

                moeda = Moeda(x, y, valor)
                todos.add(moeda)
                moedas_no_chao.add(moeda)

                tiro.kill()
                break

        return derrotados, pontos

    @staticmethod
    def verificar_jogador(jogador, inimigos):
        """Retorna True se o jogador levou dano neste frame."""
        houve_colisao = False

        for inimigo in list(inimigos):
            hitbox = getattr(inimigo, "hitbox", inimigo.rect)

            if jogador.rect.colliderect(hitbox):
                houve_colisao = True

                # O chefe nao some ao encostar no jogador (antes morria
                # instantaneamente); so os inimigos comuns sao destruidos.
                if not (isinstance(inimigo, Raposa) and inimigo.gigante):
                    inimigo.kill()

        if houve_colisao:
            return jogador.receber_dano()

        return False

    @staticmethod
    def verificar_bolas(jogador, bolas):
        """Bolas do Atirador. Retorna True se o jogador levou dano."""
        for bola in list(bolas):
            if jogador.rect.colliderect(bola.rect.inflate(-6, -6)):
                bola.kill()
                if jogador.receber_dano():
                    return True
        return False
