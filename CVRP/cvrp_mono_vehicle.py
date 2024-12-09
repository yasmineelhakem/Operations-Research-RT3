import gurobipy as grb
import numpy as np

# Paramètres
N = 5 # Nombre de clients
Q = 15  # Capacité des véhicules
d = [0, 2, 4, 5, 3]  # Demandes des clients (index 0 est le dépôt)
D = np.array([[0, 10, 15, 20, 25],
              [10, 0, 35, 25, 30],
              [15, 35, 0, 30, 15],
              [20, 25, 30, 0, 40],
              [25, 30, 15, 40, 0]])  # Matrice de distance entre clients

# Créer un modèle Gurobi
model = grb.Model("CVRP")

# Variables de décision : x[i,j] = 1 si le véhicule va de i à j
x = {}
for i in range(N):
    for j in range(N):
        if i != j:
            x[i, j] = model.addVar(vtype=grb.GRB.BINARY, name=f"x_{i}_{j}")

# Variables pour éviter les sous-cycles : u[i] est la quantité transportée après avoir visité i
u = {}
for i in range(1, N):
    u[i] = model.addVar(vtype=grb.GRB.CONTINUOUS, name=f"u_{i}")

# Fonction objectif : minimiser la distance totale parcourue
model.setObjective(grb.quicksum(D[i, j] * x[i, j] for i in range(N) for j in range(N) if i != j), grb.GRB.MINIMIZE)

# Contraintes
# Chaque client doit être visité exactement une fois
for i in range(1, N):
    model.addConstr(grb.quicksum(x[i, j] for j in range(N) if i != j) == 1, f"Visit_once_{i}")
    model.addConstr(grb.quicksum(x[j, i] for j in range(N) if i != j) == 1, f"Leave_once_{i}")

# La capacité des véhicules ne doit pas être dépassée
for j in range(1, N):
    model.addConstr(grb.quicksum(d[i] * x[i, j] for i in range(N) if i != j) <= Q, f"Capacity_{j}")

# Eviter les sous-cycles
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            model.addConstr(u[i] - u[j] + (N - 1) * x[i, j] <= N - 2, f"No_subcycle_{i}_{j}")

# Optimisation
model.optimize()

# Affichage des résultats
if model.status == grb.GRB.OPTIMAL:
    print("Solution optimale trouvée :")
    for i in range(N):
        for j in range(N):
            if i != j and x[i, j].x > 0.5:  # Si x[i, j] est proche de 1
                print(f"Le véhicule va de {i} à {j}")
else:
    print("Aucune solution optimale trouvée.")
