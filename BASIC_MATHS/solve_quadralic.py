import math


def solve_quadralic(a, b, c):
    if a == 0:
        return None

    discriminant = b**2 - 4 * a * c

    if discriminant > 0:
        # Two real roots exist
        root1 = (-b - math.sqrt(discriminant)) / (2 * a)
        root2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return root1, root2

    elif discriminant == 0:
        # One real root exists
        root = -b / (2 * a)
        return root

    else:
        # No real roots exist
        real_part = -b / (2 * a)
        imaginary_part = math.sqrt(-discriminant) / (2 * a)
        return (real_part + imaginary_part * 1j), (real_part - imaginary_part * 1j)
