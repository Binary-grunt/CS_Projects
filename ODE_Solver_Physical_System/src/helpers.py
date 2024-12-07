import argparse
from systems import create_double_pendulum, create_lotka_volterra, create_heat_equation_1d
from solvers import EulerSolver, RungeKuttaSolver, VerletSolver
from utils import generate_initial_conditions


def parse_arguments():
    """
    Handles the command-line interface configuration and returns the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Differential Equations Solver for Physical Systems")
    parser.add_argument("--system", choices=["double_pendulum", "lotka_volterra", "heat_equation_1d"],
                        required=True, help="Physical system to simulate.")
    parser.add_argument("--solver", choices=["euler", "runge_kutta", "verlet"], required=True,
                        help="Numerical method to use.")
    parser.add_argument("--t_end", type=float, required=True, help="Duration of the simulation.")
    parser.add_argument("--dt", type=float, required=True, help="Time step.")
    parser.add_argument("--output", type=str, help="Path to save the results (CSV).")
    parser.add_argument("--animate", action="store_true", help="Create an animation of the results.")
    return parser.parse_args()


def get_system_and_initial_conditions(system_name):
    """
    Returns the physical system, initial conditions, and labels based on the selection.
    """
    if system_name == "double_pendulum":
        system = create_double_pendulum()
        initial_conditions = [3.14 / 4, 3.14 / 2, 0, 0]  # [θ1, θ2, ω1, ω2]
        labels = ["θ1", "θ2", "ω1", "ω2"]
    elif system_name == "lotka_volterra":
        system = create_lotka_volterra()
        initial_conditions = [40, 9]  # [prey, predators]
        labels = ["Prey", "Predators"]
    elif system_name == "heat_equation_1d":
        system = create_heat_equation_1d()
        initial_conditions = generate_initial_conditions(size=100, method="random", low=0, high=100)
        labels = [f"T(x{i})" for i in range(len(initial_conditions))]
    else:
        raise ValueError(f"Unknown system: {system_name}")
    return system, initial_conditions, labels


def get_solver(solver_name, system_name):
    """
    Returns the appropriate solver class.
    """
    if solver_name == "euler":
        return EulerSolver
    elif solver_name == "runge_kutta":
        return RungeKuttaSolver
    elif solver_name == "verlet":
        if system_name != "double_pendulum":
            raise ValueError("The Verlet solver is only compatible with mechanical systems.")
        return VerletSolver
    else:
        raise ValueError(f"Unknown solver: {solver_name}")
