import math


def calculate_binomial_coefficient(n: int, k: int) -> int:
    """Calculate the binomial coefficient (n choose k)."""
    if k < 0 or k > n:
        raise ValueError("k must be in the range 0 <= k <= n.")
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def compute_newton_term(a: int, b: int, n: int, k: int) -> int:
    """Compute the k-th term of the Newton expansion of (a + b) ** n."""
    coefficient = calculate_binomial_coefficient(n, k)
    power_a = a ** (n - k)
    power_b = b ** k
    return coefficient * power_a * power_b


def generate_newton_expansion(a: int, b: int, n: int) -> str:
    """Generate the symbolic Newton expansion of (a + b) ** n."""
    terms = []
    for k in range(n + 1):
        coefficient = calculate_binomial_coefficient(n, k)
        term = f"{coefficient}*a^{n - k}*b^{k}" if coefficient != 1 else f"a^{n - k}*b^{k}"
        term = term.replace("*a^0", "").replace("*b^0", "")
        term = term.replace("a^1*", "a*").replace("b^1*", "b*").replace("^1", "")
        terms.append(term)
    return " + ".join(terms)


def display_newton_expansion(a: int, b: int, n: int) -> None:
    """Display the Newton expansion of (a + b) ** n."""
    print(f"The Newton expansion of ({a} + {b})^{n} is:")
    print(generate_newton_expansion(a, b, n))
