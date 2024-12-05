import math


def calculate_binomial_coefficient(n: int, k: int) -> int:
    """ Calculate the binomial coefficient (n choose k) """
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def compute_newton_term(a: int, b: int, n: int, k: int) -> int:
    """ Compute the k-th term of the Newton expansion of (a + b) ** n """
    coefficient = calculate_binomial_coefficient(n, k)
    power_a = a ** (n - k)
    power_b = b ** k
    return coefficient * power_a * power_b


def display_newton_expansion(a: int, b: int, n: int) -> None:
    """ Display the Newton expansion of (a + b) ** n """
    for k in range(n + 1):
        term = compute_newton_term(a, b, n, k)
        print(f"Term {k}: {term}")
