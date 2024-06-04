from sympy.ntheory import discrete_log

# Given values
p = 2476099
g = 2
A = 1901473

# Solve for a
a = discrete_log(p, A, g)
print(f"Private key a: {a}")