from constantes import ARQUIVO_RECORDE


def carregar_recorde():
    try:
        with open(ARQUIVO_RECORDE, "r") as arquivo:
            return int(arquivo.read().strip())
    except (OSError, ValueError):
        return 0


def salvar_recorde(pontos):
    """Salva se for maior que o recorde atual. Retorna True se bateu o recorde."""
    if pontos > carregar_recorde():
        try:
            with open(ARQUIVO_RECORDE, "w") as arquivo:
                arquivo.write(str(pontos))
        except OSError:
            return False
        return True
    return False
