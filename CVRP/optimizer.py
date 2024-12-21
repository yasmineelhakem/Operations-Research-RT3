import gurobipy as grb
def solve_cvrp(N, Q, K, d, D):

    try:
        model = grb.Model("CVRP")

        # Decision variables
        #1. Binary variables: x[i, j, k] = 1 if vehicle k travels from i to j sinon x[i, j, k] = 0
        x = {}
        for i in range(N):
            for j in range(N):
                if i != j:
                    for k in range(K):
                        x[i, j, k] = model.addVar(vtype=grb.GRB.BINARY, name=f"x_{i}_{j}_{k}")

        #2.  Vehicle load after it has visted each client
        u = {}
        for i in range(1, N):
            for k in range(K):
                u[i, k] = model.addVar(vtype=grb.GRB.CONTINUOUS, name=f"u_{i}_{k}")

        # Objective function: Minimize total travel distance by all vehicles
        model.setObjective(
            grb.quicksum(D[i, j] * x[i, j, k] for i in range(N) for j in range(N) if i != j for k in range(K)),
            grb.GRB.MINIMIZE
        )

        # Constraints
        # 1. Each customer must be visited exactly once by any vehicle and leaved once
        for i in range(1, N):
            model.addConstr(
                grb.quicksum(x[i, j, k] for j in range(N) if i != j for k in range(K)) == 1, f"Visit_once_{i}"
            )
            model.addConstr(
                grb.quicksum(x[j, i, k] for j in range(N) if i != j for k in range(K)) == 1, f"Leave_once_{i}"
            )

        # 2. Capacity constraints: Load on each vehicle must not exceed its capacity
        for k in range(K):
            for j in range(1, N):
                model.addConstr(
                    grb.quicksum(d[i] * x[i, j, k] for i in range(N) if i != j) <= Q, f"Capacity_{j}_{k}"
                )

        # 3. Subtour elimination (MTZ constraints)
        # a vehicle dont repeat a route visited by other vehicle ensuring that all nodes are connected into a single route per vehicle.
        for i in range(1, N):
            for j in range(1, N):
                if i != j:
                    for k in range(K):
                        model.addConstr(
                            u[i, k] - u[j, k] + Q * x[i, j, k] <= Q - d[j], f"No_subcycle_{i}_{j}_{k}"
                        )

        # 4. Load consistency: Load at depot is 0, and load evolves as demands are met
        for k in range(K):
            for i in range(1, N):
                model.addConstr(u[i, k] >= d[i] * grb.quicksum(x[0, i, k] for j in range(N) if i != j), f"Load_{i}_{k}")

        # 5. Flow conservation: If a vehicle arrives at a customer, it must also leave
        for k in range(K):
            for j in range(1, N):
                model.addConstr(
                    grb.quicksum(x[i, j, k] for i in range(N) if i != j) == grb.quicksum(x[j, i, k] for i in range(N) if i != j),
                    f"Flow_{j}_{k}"
                )

        model.optimize()

        if model.status == grb.GRB.OPTIMAL:
            routes = {k: [] for k in range(K)}
            for k in range(K):
                for i in range(N):
                    for j in range(N):
                        if i != j and x[i, j, k].x > 0.5:  # If x[i, j, k] is close to 1
                            routes[k].append((i, j))
            return {"status": "Optimal", "routes": routes, "total_distance": model.objVal}
        else:
            return {"status": "No solution found", "routes": None, "total_distance": None}

    except Exception as e:
        return {"status": f"Error: {e}", "routes": None, "total_distance": None}
