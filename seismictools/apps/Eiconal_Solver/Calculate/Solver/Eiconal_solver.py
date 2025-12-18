import numpy as np
from numba import jit



@jit(nopython=True)
def gradient_point(model: np.ndarray, x: float, z: float, delta: float) -> np.ndarray:
    n_x = int(x // delta)
    n_z = int(z // delta)
    nz, nx = model.shape

    if n_x == 0:
        res_x = (model[n_z][n_x + 1] - model[n_z][n_x]) / delta
    else:
        res_x = (model[n_z][n_x + 1] - model[n_z][n_x - 1]) / (2 * delta)

    if n_z == 0:
        res_z = (model[n_z + 1][n_x] - model[n_z][n_x]) / delta
    else:
        res_z = (model[n_z + 1][n_x] - model[n_z - 1][n_x]) / (2 * delta)

    return np.array([res_x, res_z])


@jit(nopython=True)
def gradient_field(model: np.ndarray, delta: float) -> np.ndarray:
    rows, cols = model.shape
    res = np.zeros((rows-1, cols-1, 2))
    for i in range(len(model) - 1):
        for j in range(len(model[i]) - 1):
            res[i][j] = gradient_point(model=model, x=delta*j, z=delta*i, delta=delta)
    return res


@jit(nopython=True)
def trajectory_calculator(v_model: np.ndarray, x_0: float, z_0: float, theta: float, delta: float) -> np.ndarray:

    slowness_grad_field = gradient_field(model=v_model**(-1), delta=delta)

    n_x_0 = int(x_0 // delta)
    n_z_0 = int(z_0 // delta)

    p_0 = [np.cos(theta) / v_model[n_z_0][n_x_0], np.sin(theta) / v_model[n_z_0][n_x_0]]

    trajectory = [[x_0, z_0]]
    p = [p_0]

    while True:
        n_x = int(trajectory[-1][0] // delta)
        n_z = int(trajectory[-1][1] // delta)

        if  n_x >= slowness_grad_field.shape[1] or n_z >= slowness_grad_field.shape[0] or n_z < 0 or n_x < 0:
            break

        p.append([p[-1][0] + delta * slowness_grad_field[n_z][n_x][0], p[-1][1] + delta * slowness_grad_field[n_z][n_x][1]])

        dx = delta * v_model[n_z][n_x] * p[-1][0]
        dz = delta * v_model[n_z][n_x] * p[-1][1]
        #if delta * v_model[n_z][n_x] * p[-1][0] <= delta/1000:
            #dx = 0.0
        #if delta * v_model[n_z][n_x] * p[-1][1] <= delta/1000:
            #dz = 0.0
        trajectory.append([trajectory[-1][0] + dx, trajectory[-1][1] + dz])

    trajectory = np.array(trajectory)
    return trajectory