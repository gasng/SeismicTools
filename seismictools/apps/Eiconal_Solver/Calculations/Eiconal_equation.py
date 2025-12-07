import numpy as np

class EiconalEquationSolving:

    @staticmethod
    def gradient_point(v_model: np.ndarray, x: float, z: float, delta: float) -> np.ndarray:
        n_x = int(x//delta)
        n_z = int(z//delta)
        res_x = (v_model[n_z][n_x+1] - v_model[n_z][n_x]) / delta
        res_z = (v_model[n_z+1][n_x] - v_model[n_z][n_x]) / delta
        return np.array([res_x, res_z])

    @staticmethod
    def gradient_field(v_model: np.ndarray, delta: float) -> np.ndarray:
        rows, cols = v_model.shape
        res = np.zeros((rows-1, cols-1, 2))
        for i in range(len(v_model) - 1):
            for j in range(len(v_model[i]) - 1):
                res[i][j] = EiconalEquationSolving.gradient_point(v_model=v_model, x=delta*j, z=delta*i, delta=delta)
        return res

    @staticmethod
    def trajectory_calculator(v_model: np.ndarray, x_0: float, z_0: float, theta: float, delta: float) -> np.ndarray:
        slowness_grad_field = EiconalEquationSolving.gradient_field(v_model ** (-1))

        n_x_0 = int(x_0 // delta)
        n_z_0 = int(z_0 // delta)
        p_0 = [np.cos(theta) / v_model[n_x_0][n_z_0], np.sin(theta) / v_model[n_x_0][n_z_0]]

        trajectory = [[x_0, z_0]]
        p = [p_0]

        while True:
            n_x = int(trajectory[-1][0] // delta)
            n_z = int(trajectory[-1][1] // delta)
            p.append([p[-1][0] + delta * slowness_grad_field[n_x][n_z], p[-1][1] + delta * slowness_grad_field[n_x][n_z]])
            trajectory.append([trajectory[-1][0] + delta * v_model[n_x][n_z] * p[-1][0], trajectory[-1][1] + delta * v_model[n_x][n_z] * p[-1][1]])

        trajectory = np.array(trajectory)
        return trajectory