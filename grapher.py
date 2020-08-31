import pygame
import threading
from solver import Solver


class Grapher:
    # Variables del graficador
    screen: pygame.surface.Surface
    done: bool

    def __init__(self, state):
        # Inicializando visualizador
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Graficador tablas y cortes")
        self.done = False

        self.state = state

        self.solver = Solver(state)
        self.t = threading.Thread(target=self.solver.best_first)
        self.t.start()

    def run(self):
        while not self.done:
            # Actualizando eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    continue

            self.screen.fill((33, 33, 33))
            self.draw_cuts()
            pygame.display.update()

    def draw_cuts(self):
        MARGEN = 10
        HEIGHT = 10
        SCALE = 10
        y = MARGEN

        # Dibujando planks
        pl = self.solver.actual_state.pl / SCALE
        for i in range(len(self.solver.actual_state.planks)):
            pygame.draw.rect(self.screen, (60, 33, 33),
                             (MARGEN, MARGEN * (i + 1) + HEIGHT * i, pl, HEIGHT))

        # Dibujando cortes
        for l_cuts in self.solver.actual_state.cuts:
            x = MARGEN
            for cut in l_cuts:
                cut = cut / SCALE
                pygame.draw.rect(self.screen, (100, 100, 100),
                                 (x, y, cut, HEIGHT))
                pygame.draw.line(self.screen, (200, 200, 200),
                                 (x + cut - 1, y), (x + cut - 1, y + HEIGHT), 1)
                x += cut
            y += MARGEN + HEIGHT

        # Dibujando cortes faltantes
        x = MARGEN
        y = MARGEN
        for cut in self.solver.actual_state.dims:
            cut = cut / SCALE
            real_y = self.screen.get_height() - y
            pygame.draw.rect(self.screen, (100, 100, 100),
                             (x, real_y, cut, HEIGHT / 2))
            y += MARGEN + HEIGHT / 2

    def set_state(self, state):
        self.state = state

    def close(self):
        self.done = True
        self.t.join()
        print("Fin del graficador")

    def wait(self):
        self.t.join()
