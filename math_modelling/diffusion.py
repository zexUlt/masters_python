from typing import Callable
import numpy as np

from exceptions import FunctionNotInitialized

class DiffusionSolver:
    def __init__(self, N: int, T: int, tau: float, D: float) -> None:
        self.D = D
        self.N = N
        self.h = 2*np.pi / N
        self.X = np.linspace(0, 2*np.pi, N)
        self.t = np.linspace(0, T, T/tau) 
        # Вектор собственных значений надо будет переформатировать ->
        # -> [-N/2, ..., -1, 0, 1, ..., N/2]
        self.eigenvals = np.array(
            [4*self.D / self.h**2 * np.sin(k*self.h/4) for k in range(N)]
            )
        self.__reconstruct_eigenvals_array__()
    
    def __reconstruct_eigenvals_array__(self):
        reversed_half = self.X[self.N/2:]
        reversed_half = reversed_half[::-1]
        self.eigenvals = np.append(reversed_half, self.eigenvals[:self.N/2])

    def run(self) -> None:
        if not self.U0:
            raise FunctionNotInitialized(f'Function U0 should be set before running solver.')
        
        u = self.U0(self.X)
        Fu = np.fft.fft(u)


    def set_F_function(self, F: Callable) -> None:
        if callable(F):
            self.F = np.vectorize(F)
        else:
            raise TypeError(f"Argument should be callable. Got {type(F)}.")
    
    def set_U0_function(self, U0: Callable) -> None:
        if callable(U0):
            self.U0 = np.vectorize(U0)
        else: 
            raise TypeError(f"Argument should be callable. Got {type(U0)}.")