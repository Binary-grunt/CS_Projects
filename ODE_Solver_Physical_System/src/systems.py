import numpy as np

# HACK : Brutal force here, Refactor to it later


class PhysicalSystem:
    """
    Base class to represent a physical system.
    """

    def __init__(self, equations, params):
        """
        Initializes the physical system.
        :param equations: Function representing the system's ODEs.
        :param params: Dictionary of the system's physical parameters.
        """
        self.equations = equations
        self.params = params

    def get_equations(self):
        """
        Returns the ODE function.
        """
        return lambda t, y: self.equations(t, y, self.params)


# Specific physical systems
def double_pendulum(t, state, params):
    """
    Differential equations for a double pendulum.
    :param t: Current time (not used here but required for compatibility).
    :param state: Current state [θ1, θ2, ω1, ω2].
    :param params: Dictionary containing the physical parameters.
    :return: Derivatives [dθ1/dt, dθ2/dt, dω1/dt, dω2/dt].
    """
    g, l1, l2, m1, m2 = params['g'], params['l1'], params['l2'], params['m1'], params['m2']
    θ1, θ2, ω1, ω2 = state

    delta = θ2 - θ1

    # Intermediate calculations for the equations of motion
    den1 = (m1 + m2) * l1 - m2 * l1 * np.cos(delta)**2
    den2 = (l2 / l1) * den1

    dω1_dt = (m2 * l1 * ω1**2 * np.sin(delta) * np.cos(delta) +
              m2 * g * np.sin(θ2) * np.cos(delta) +
              m2 * l2 * ω2**2 * np.sin(delta) -
              (m1 + m2) * g * np.sin(θ1)) / den1

    dω2_dt = (-m2 * l2 * ω2**2 * np.sin(delta) * np.cos(delta) +
              (m1 + m2) * g * np.sin(θ1) * np.cos(delta) -
              (m1 + m2) * l1 * ω1**2 * np.sin(delta) -
              (m1 + m2) * g * np.sin(θ2)) / den2

    dθ1_dt = ω1
    dθ2_dt = ω2

    return np.array([dθ1_dt, dθ2_dt, dω1_dt, dω2_dt])


def lotka_volterra(t, state, params):
    """
    Differential equations for the Lotka-Volterra model (predator-prey).
    :param t: Current time.
    :param state: Current state [prey, predators].
    :param params: Dictionary containing the parameters {a, b, c, d}.
    :return: Derivatives [d(prey)/dt, d(predator)/dt].
    """
    prey, predator = state
    a, b, c, d = params['a'], params['b'], params['c'], params['d']

    dprey_dt = a * prey - b * prey * predator
    dpredator_dt = c * prey * predator - d * predator

    return np.array([dprey_dt, dpredator_dt])


def heat_equation_1d(t, state, params):
    """
    1D heat equation.
    :param t: Current time.
    :param state: Current state (temperature distribution).
    :param params: Dictionary containing the parameters {alpha, dx}.
    :return: New temperature gradient (time derivative).
    """
    alpha, dx = params['alpha'], params['dx']
    dT_dt = np.zeros_like(state)

    # Spatial discretization (finite difference method)
    for i in range(1, len(state) - 1):
        dT_dt[i] = alpha * (state[i - 1] - 2 * state[i] + state[i + 1]) / dx**2

    return dT_dt


# Create instances for physical systems
def create_double_pendulum():
    """
    Initializes a double pendulum with default parameters.
    """
    params = {
        'g': 9.81,   # Gravity (m/s²)
        'l1': 1.0,   # Length of the first pendulum (m)
        'l2': 1.0,   # Length of the second pendulum (m)
        'm1': 1.0,   # Mass of the first pendulum (kg)
        'm2': 1.0    # Mass of the second pendulum (kg)
    }
    return PhysicalSystem(double_pendulum, params)


def create_lotka_volterra():
    """
    Initializes a Lotka-Volterra model with default parameters.
    """
    params = {
        'a': 0.1,    # Growth rate of prey
        'b': 0.02,   # Predation rate
        'c': 0.01,   # Efficiency of converting prey into predators
        'd': 0.1     # Mortality rate of predators
    }
    return PhysicalSystem(lotka_volterra, params)


def create_heat_equation_1d():
    """
    Initializes a 1D heat equation with default parameters.
    """
    params = {
        'alpha': 0.01,  # Thermal diffusivity
        'dx': 0.1       # Spatial discretization
    }
    return PhysicalSystem(heat_equation_1d, params)
