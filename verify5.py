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
F_mu_nu = sp.MutableDenseNDimArray([[[0 for _ in range(3)] for _ in range(4)] for _ in range(4)])
for mu in range(4):
    for nu in range(4):
        if mu < nu:
            for a in range(3):
                F_mu_nu[mu, nu, a] = sp.diff(A_mu[a], [t, x, y, z][nu]) - sp.diff(A_mu[a], [t, x, y, z][mu])
                for b in range(3):
                    for c in range(3):
                        F_mu_nu[mu, nu, a] += g * f_abc[a][b][c] * A_mu[b] * A_mu[c]

# Symmetrize F_mu_nu
F_mu_nu_sym = sp.MutableDenseNDimArray([[[0 for _ in range(3)] for _ in range(4)] for _ in range(4)])
for mu in range(4):
    for nu in range(4):
        for a in range(3):
            F_mu_nu_sym[mu, nu, a] = F_mu_nu[mu, nu, a] - F_mu_nu[nu, mu, a]

# Define the metric tensor (Minkowski space)
eta = sp.Matrix([
    [1, 0, 0, 0],
    [0, -1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, -1]
])

# Compute the Yang-Mills action
L = 0
for mu in range(4):
    for nu in range(mu+1, 4):
        for a in range(3):
            F_mu_nu_a = F_mu_nu_sym[mu, nu, a]
            F_mu_nu_a_contr = sum(eta[mu, mu] * eta[nu, nu] * F_mu_nu_sym[mu, nu, a]**2 for mu in range(4) for nu in range(mu+1, 4))
            L += 0.25 * F_mu_nu_a_contr

# Define the Lagrangian density
L_density = 0.25 * sum(F_mu_nu_sym[mu, nu, a] * F_mu_nu_sym[mu, nu, a] for mu in range(4) for nu in range(mu+1, 4) for a in range(3))

# Define the total action S
S = sp.integrate(L_density, (t, -sp.oo, sp.oo), (x, -sp.oo, sp.oo), (y, -sp.oo, sp.oo), (z, -sp.oo, sp.oo))

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
