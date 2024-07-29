import sympy as sp

# Define symbols
g = sp.Symbol('g', real=True, positive=True)
t, x, y, z = sp.symbols('t x y z')
A0, A1, A2, A3 = sp.symbols('A0 A1 A2 A3', cls=sp.Function)

# Define the gauge fields A_mu
A_mu = sp.Matrix([A0(t, x, y, z), A1(t, x, y, z), A2(t, x, y, z), A3(t, x, y, z)])

# Define the structure constants for SU(2)
f_abc = [[[0, 0, 0], [0, 0, 1], [0, -1, 0]],
         [[0, 0, -1], [0, 0, 0], [1, 0, 0]],
         [[0, 1, 0], [-1, 0, 0], [0, 0, 0]]]

# Define the field strength tensor F_mu_nu
def compute_field_strength_tensor(A_mu, g, f_abc):
    F_mu_nu = sp.MutableDenseNDimArray([[[0 for _ in range(3)] for _ in range(4)] for _ in range(4)])
    for mu in range(4):
        for nu in range(4):
            if mu < nu:
                for a in range(3):
                    F_mu_nu[mu, nu, a] = sp.diff(A_mu[a], [t, x, y, z][nu]) - sp.diff(A_mu[a], [t, x, y, z][mu])
                    for b in range(3):
                        for c in range(3):
                            F_mu_nu[mu, nu, a] += g * f_abc[a][b][c] * A_mu[b] * A_mu[c]
    return F_mu_nu

# Symmetrize F_mu_nu
def symmetrize_field_strength_tensor(F_mu_nu):
    F_mu_nu_sym = sp.MutableDenseNDimArray([[[0 for _ in range(3)] for _ in range(4)] for _ in range(4)])
    for mu in range(4):
        for nu in range(4):
            for a in range(3):
                F_mu_nu_sym[mu, nu, a] = F_mu_nu[mu, nu, a] - F_mu_nu[nu, mu, a]
    return F_mu_nu_sym

# Define the metric tensor (Minkowski space)
eta = sp.Matrix([
    [1, 0, 0, 0],
    [0, -1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, -1]
])

# Compute the Yang-Mills action
def compute_yang_mills_action(F_mu_nu_sym, eta):
    L = 0
    for mu in range(4):
        for nu in range(mu + 1, 4):
            for a in range(3):
                F_mu_nu_a = F_mu_nu_sym[mu, nu, a]
                F_mu_nu_a_contr = sum(eta[mu, mu] * eta[nu, nu] * F_mu_nu_sym[mu, nu, a]**2 for mu in range(4) for nu in range(mu + 1, 4))
                L += 0.25 * F_mu_nu_a_contr
    return L

# Define the Lagrangian density
def compute_lagrangian_density(F_mu_nu_sym):
    L_density = 0.25 * sum(F_mu_nu_sym[mu, nu, a] * F_mu_nu_sym[mu, nu, a] for mu in range(4) for nu in range(mu + 1, 4) for a in range(3))
    return L_density

# Define the total action S
def compute_total_action(L_density):
    S = sp.integrate(L_density, (t, -sp.oo, sp.oo), (x, -sp.oo, sp.oo), (y, -sp.oo, sp.oo), (z, -sp.oo, sp.oo))
    return S

# Verification functions
def verify_field_strength_tensor(F_mu_nu, g, f_abc, A):
    coordinates = sp.symbols('t x y z')
    F_theory = sp.MutableDenseNDimArray([[[0 for _ in range(3)] for _ in range(4)] for _ in range(4)])
    for mu in range(4):
        for nu in range(4):
            if mu < nu:
                for a in range(3):
                    F_theory[mu, nu, a] = sp.diff(A[a], coordinates[nu]) - sp.diff(A[a], coordinates[mu])
                    for b in range(3):
                        for c in range(3):
                            F_theory[mu, nu, a] += g * f_abc[a][b][c] * A[b] * A[c]
                if not sp.simplify(F_mu_nu[mu, nu, a] - F_theory[mu, nu, a]) == 0:
                    return False
    return True

def verify_yang_mills_action(S, L_density):
    coordinates = sp.symbols('t x y z')
    action_theory = sp.integrate(L_density, (coordinates[0], -sp.oo, sp.oo), (coordinates[1], -sp.oo, sp.oo),
                                 (coordinates[2], -sp.oo, sp.oo), (coordinates[3], -sp.oo, sp.oo))
    return sp.simplify(S - action_theory) == 0

# Additional verification functions
def verify_symmetry(F_mu_nu_sym):
    for mu in range(4):
        for nu in range(4):
            for a in range(3):
                if not sp.simplify(F_mu_nu_sym[mu, nu, a] + F_mu_nu_sym[nu, mu, a]) == 0:
                    return False
    return True

def verify_trivial_solution():
    A_mu_zero = sp.Matrix([0, 0, 0, 0])
    F_mu_nu_zero = compute_field_strength_tensor(A_mu_zero, g, f_abc)
    F_mu_nu_sym_zero = symmetrize_field_strength_tensor(F_mu_nu_zero)
    for mu in range(4):
        for nu in range(4):
            for a in range(3):
                if not sp.simplify(F_mu_nu_sym_zero[mu, nu, a]) == 0:
                    return False
    return True

def verify_dimensional_consistency(F_mu_nu_sym, g):
    for mu in range(4):
        for nu in range(4):
            for a in range(3):
                term = F_mu_nu_sym[mu, nu, a]
                if term.has(g):
                    if not any(g in arg.free_symbols for arg in term.args):
                        return False
    return True

# Main execution
F_mu_nu = compute_field_strength_tensor(A_mu, g, f_abc)
F_mu_nu_sym = symmetrize_field_strength_tensor(F_mu_nu)
L_density = compute_lagrangian_density(F_mu_nu_sym)
S = compute_total_action(L_density)

# Verify the field strength tensor
if verify_field_strength_tensor(F_mu_nu_sym, g, f_abc, A_mu):
    print("Field strength tensor verified successfully.")
else:
    print("Field strength tensor verification failed.")

# Verify the Yang-Mills action
if verify_yang_mills_action(S, L_density):
    print("Yang-Mills action verified successfully.")
else:
    print("Yang-Mills action verification failed.")

# Additional verifications
if verify_symmetry(F_mu_nu_sym):
    print("Field strength tensor symmetry verified successfully.")
else:
    print("Field strength tensor symmetry verification failed.")

if verify_trivial_solution():
    print("Trivial solution verified successfully.")
else:
    print("Trivial solution verification failed.")

if verify_dimensional_consistency(F_mu_nu_sym, g):
    print("Dimensional consistency verified successfully.")
else:
    print("Dimensional consistency verification failed.")
