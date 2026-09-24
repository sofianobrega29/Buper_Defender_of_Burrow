import pygame

class TrilhaPrincipal:
    def __init__(self, caminho, estado = True):
        self.camminho = caminho
        self.estado = estado

    def play(self):
        if self.estado:
            pygame.mixer.music.load(self.camminho)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)

class Som:
    def __init__(self, caminho, estado = True):
        self.caminho = caminho
        self.estado = estado

        self.som = pygame.mixer.Sound(self.caminho)
        self.som.set_volume(1)
            
    def play(self):
        if self.estado:
            self.som.play()

class Estilingue(Som):
    def __init__(self, caminho, estado=True):
        super().__init__(caminho, estado)
    

class Cachorro(Som):
    def __init__(self, caminho, estado=True):
        super().__init__(caminho, estado)
    
