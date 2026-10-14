import random

from constantes import LARGURA
from inimigos.inimigo_padrao import InimigoPadrao
from inimigos.inimigo_veloz import InimigoVeloz
from inimigos.inimigo_ziguezague import InimigoZigueZague
from inimigos.inimigo_tanque import InimigoTanque
from inimigos.inimigo_atirador import InimigoAtirador
from inimigos.inimigo_investida import InimigoInvestida
from inimigos.raposa import Raposa

# onda em que cada tipo comeca a aparecer, com seu "peso" no sorteio
TIPOS = [
    (InimigoPadrao, 1, 6),
    (InimigoVeloz, 2, 3),
    (InimigoZigueZague, 3, 3),
    (InimigoTanque, 4, 2),
    (InimigoInvestida, 5, 2),
    (InimigoAtirador, 6, 3),
]

# ondas com chefe -> vida do chefe
CHEFES = {5: 40, 10: 90}


class GerenciadorOndas:
    def __init__(self, todos, inimigos, jogador, bolas=None):
        self.todos = todos
        self.inimigos = inimigos
        self.jogador = jogador
        self.bolas = bolas  # grupo das bolas disparadas pelos atiradores

        self.wave = 1
        self.max_waves = 10
        self.concluido = False
        self.chefe_criado = False

        self.inimigos_wave = 5
        self.inimigos_spawnados = 0
        self.spawn_timer = 0
        self.intervalo_spawn = 90

    @property
    def onda_de_chefe(self):
        return self.wave in CHEFES

    def atualizar(self):
        if self.concluido:
            return

        self.spawn_timer += 1

        # So avanca quando todos os inimigos da onda foram derrotados.
        if (
            self.inimigos_spawnados >= self.inimigos_wave
            and len(self.inimigos) == 0
        ):
            if self.wave >= self.max_waves:
                self.concluido = True
                return

            self.wave += 1
            self.inimigos_wave += 2
            self.inimigos_spawnados = 0
            self.spawn_timer = 0
            self.chefe_criado = False
            self.intervalo_spawn = max(40, self.intervalo_spawn - 4)

        if (
            self.inimigos_spawnados < self.inimigos_wave
            and self.spawn_timer >= self.intervalo_spawn
        ):
            self._criar_inimigos()
            self.inimigos_spawnados += 1
            self.spawn_timer = 0

    def _sortear_tipo(self):
        disponiveis = [(c, p) for c, onda, p in TIPOS if self.wave >= onda]
        classes = [c for c, _ in disponiveis]
        pesos = [p for _, p in disponiveis]
        return random.choices(classes, weights=pesos, k=1)[0]

    def _criar_inimigos(self):
        x = random.randint(60, LARGURA - 60)
        self._adicionar(self._sortear_tipo()(x, -35))

        # Raposa perseguidora a cada 5 inimigos (a partir da onda 3).
        # Nas ondas de chefe, a primeira delas e o chefe gigante.
        if self.wave >= 3 and self.inimigos_spawnados % 5 == 4:
            gigante = self.onda_de_chefe and not self.chefe_criado
            if gigante:
                self.chefe_criado = True

            raposa = Raposa(
                random.randint(100, LARGURA - 100),
                -60,
                gigante=gigante,
                vida_chefe=CHEFES.get(self.wave, 40),
                nome_sprite=("chefe" if self.wave == 5 else "rei") if gigante else None,
            )
            raposa.alvo = self.jogador
            self._adicionar(raposa)

    def _adicionar(self, inimigo):
        # Dificuldade progressiva nos inimigos basicos (maximo +3).
        if isinstance(inimigo, (InimigoPadrao, InimigoVeloz, InimigoZigueZague)):
            inimigo.velocidade += min(3, (self.wave - 1) // 3)

        # Inimigos que miram/perseguem precisam saber quem e o jogador.
        if hasattr(inimigo, "alvo"):
            inimigo.alvo = self.jogador
        if isinstance(inimigo, InimigoAtirador) and self.bolas is not None:
            inimigo.grupos_tiro = (self.todos, self.bolas)

        self.todos.add(inimigo)
        self.inimigos.add(inimigo)
