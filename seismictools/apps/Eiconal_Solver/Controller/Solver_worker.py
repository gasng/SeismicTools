from PySide6.QtCore import QRunnable, Slot
import numpy as np
from ..Calculate.Solver.Eiconal_solver import EiconalSolver
from .Worker_signals import WorkerSignals

class SolverWorker(QRunnable):
    def __init__(self, v_model: np.ndarray, x0: float, z0: float, theta: float, delta: float = 0.1):
        super().__init__()
        self.v_model = v_model
        self.x0 = x0
        self.z0 = z0
        self.theta = theta
        self.delta = delta
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            deg = np.degrees(self.theta)
            self.signals.message.emit(f"Расчёт траектории под углом {deg:.0f}°...")

            trajectory = EiconalSolver.trajectory_calculator(
                self.v_model, self.x0, self.z0, self.theta, self.delta
            )

            self.signals.message.emit("Траектория рассчитана.")
            self.signals.result.emit(trajectory)

        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.result.emit(None)