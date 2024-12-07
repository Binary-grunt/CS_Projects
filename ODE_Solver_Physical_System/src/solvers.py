import numpy as np


class ODESolver:
    """
    Base class for differential equation solvers.

    This class implements the general structure of a solver for ODEs,
    leaving the details of the numerical method to subclasses.

    Attributes:
        f (callable): Function representing the system dy/dt = f(t, y).
        t (float): Current time of the simulation.
        y (np.ndarray): Current state of the system.
        dt (float): Time step for integration.
    """

    def __init__(self, f, t0, y0, dt):
        """
        Initializes the solver.
        :raises ValueError: If input types or dimensions are invalid.
        """
        if not callable(f):
            raise ValueError("The parameter 'f' must be a callable function.")
        if not isinstance(t0, (int, float)):
            raise ValueError("The parameter 't0' must be a number (int or float).")
        if not isinstance(dt, (int, float)) or dt <= 0:
            raise ValueError("The parameter 'dt' must be a positive number.")
        self.f = f
        self.t = t0
        self.y = np.array(y0, dtype=float)
        self.dt = dt

    def step(self):
        """
        Base method to be overridden in child classes.
        """
        raise NotImplementedError("The step() method must be implemented in a subclass.")

    def solve(self, t_end):
        """
        Solves the ODE over a given time interval.
        :param t_end: Final time.
        :return: Tuple (times, solutions) where:
            - times is a list of time instants.
            - solutions is a list of corresponding values.
        """
        times = [self.t]
        solutions = [self.y.copy()]
        while self.t < t_end:
            if self.t + self.dt > t_end:  # Adjust the last step to avoid overshooting t_end
                self.dt = t_end - self.t
            self.step()
            times.append(self.t)
            solutions.append(self.y.copy())
        return np.array(times), np.array(solutions)


class EulerSolver(ODESolver):
    """
    Implementation of the Euler method.
    """

    def step(self):
        """
        Advances one step using the Euler method.
        """
        self.y += self.dt * self.f(self.t, self.y)
        self.t += self.dt


class RungeKuttaSolver(ODESolver):
    """
    Implementation of the 4th-order Runge-Kutta method.
    """

    def step(self):
        """
        Advances one step using the RK4 method.
        """
        k1 = self.f(self.t, self.y)
        k2 = self.f(self.t + self.dt / 2, self.y + self.dt * k1 / 2)
        k3 = self.f(self.t + self.dt / 2, self.y + self.dt * k2 / 2)
        k4 = self.f(self.t + self.dt, self.y + self.dt * k3)
        self.y += (self.dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        self.t += self.dt


class VerletSolver(ODESolver):
    """
    Implementation of the Verlet method for mechanical systems.
    Used for problems where the acceleration is defined.
    """

    def __init__(self, f, t0, y0, dt):
        """
        Initializes the Verlet solver.
        :param f: Function representing the acceleration a = f(t, y).
        :param t0: Initial time.
        :param y0: Initial conditions (numpy array [position, velocity]).
        :param dt: Time step.
        """
        super().__init__(f, t0, y0, dt)
        self.prev_y = self.y - self.dt * self.f(self.t, self.y)  # Initial estimation

    def step(self):
        """
        Advances one step using the Verlet method.
        """
        next_y = 2 * self.y - self.prev_y + self.dt**2 * self.f(self.t, self.y)
        self.prev_y = self.y
        self.y = next_y
        self.t += self.dt
