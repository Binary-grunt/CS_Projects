import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# HACK: Refactor it if necessary


def validate_params(params, required_keys):
    """
    Validates that all required parameters are present in a dictionary.
    :param params: Dictionary of parameters.
    :param required_keys: List of required keys.
    :raises ValueError: If any required key is missing.
    """
    missing_keys = [key for key in required_keys if key not in params]
    if missing_keys:
        raise ValueError(f"The following keys are missing in the parameters: {missing_keys}")


def plot_results(times, solutions, labels=None, title=None, xlabel="Time", ylabel="Values"):
    """
    Plots the results of a simulation.
    :param times: List or array of time values.
    :param solutions: Array of solutions (each column represents a variable).
    :param labels: List of variable names.
    :param title: Title of the plot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    """
    if labels is None:
        labels = [f"Variable {i}" for i in range(solutions.shape[1])]

    for i, label in enumerate(labels):
        plt.plot(times, solutions[:, i], label=label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()


def create_animation(times, solutions, labels=None, interval=50, save_path=None):
    """
    Creates an animation to visualize the results of a simulation.
    :param times: List or array of time values.
    :param solutions: Array of solutions (each column represents a variable).
    :param labels: List of variable names.
    :param interval: Interval between animation frames (in ms).
    :param save_path: Path to save the animation (optional).
    """
    # Debug: Display the backend being used
    print("Backend used:", plt.get_backend())

    # Set up labels
    if labels is None:
        labels = [f"Variable {i}" for i in range(solutions.shape[1])]

    # Create the figure
    fig, ax = plt.subplots()
    lines = [ax.plot([], [], label=label)[0] for label in labels]
    ax.set_xlim(times[0], times[-1])
    ax.set_ylim(np.min(solutions), np.max(solutions))
    ax.set_xlabel("Time")
    ax.set_ylabel("Values")
    ax.legend()
    ax.grid()

    # Update function for each frame
    def update(frame):
        for line, col in zip(lines, solutions.T):
            line.set_data(times[:frame], col[:frame])
        return lines

    # Create the animation
    anim = FuncAnimation(fig, update, frames=len(times), interval=interval, blit=True)

    # Save or display the animation
    if save_path:
        try:
            print(f"Saving animation to: {save_path}")
            anim.save(save_path, writer='ffmpeg')
            print("Animation saved successfully.")
        except Exception as e:
            print("Error saving the animation:", e)
    else:
        print("Displaying the animation...")
        plt.show()


def generate_initial_conditions(size, method="random", low=-1.0, high=1.0):
    """
    Generates initial conditions for a simulation.
    :param size: Size of the initial conditions.
    :param method: Method to generate values ("random", "zeros", "ones").
    :param low: Lower bound (for "random").
    :param high: Upper bound (for "random").
    :return: Numpy array of initial conditions.
    """
    if method == "random":
        return np.random.uniform(low, high, size)
    elif method == "zeros":
        return np.zeros(size)
    elif method == "ones":
        return np.ones(size)
    else:
        raise ValueError("Unknown method. Use 'random', 'zeros', or 'ones'.")


def save_results_to_csv(times, solutions, file_path="results.csv"):
    """
    Saves the results of a simulation to a CSV file.
    :param times: List or array of time values.
    :param solutions: Array of solutions (each column represents a variable).
    :param file_path: Path to the CSV file.
    """
    import csv
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time"] + [f"Variable {i}" for i in range(solutions.shape[1])])
        for t, sol in zip(times, solutions):
            writer.writerow([t] + list(sol))


def load_results_from_csv(file_path):
    """
    Loads simulation results from a CSV file.
    :param file_path: Path to the CSV file.
    :return: Tuple (times, solutions).
    """
    import csv
    times = []
    solutions = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the first row (headers)
        for row in reader:
            times.append(float(row[0]))
            solutions.append([float(val) for val in row[1:]])
    return np.array(times), np.array(solutions)
