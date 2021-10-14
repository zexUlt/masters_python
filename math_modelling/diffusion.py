import numpy as np


class DiffusionSolver:
    def __init__(self, N: int, T: int, tau: float, D: float):
        self.D = D
        self.h = 2*np.pi / N
        self.X = np.linspace(0, 2*np.pi, N)
        self.t = np.linspace(0, T, T/tau) 
        # Вектор собственных значений надо будет переформатировать ->
        # -> [-N/2, ..., -1, 0, 1, ..., N/2]
        self.eigenvals = np.array(
            [4*self.D / self.h**2 * np.sin(k*self.h/4) for k in range(N)]
            )