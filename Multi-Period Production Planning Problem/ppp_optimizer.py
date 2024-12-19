from gurobipy import Model, GRB

def production_planning_optimizer(periods, demand, selling_price, production_cost, storage_cost, capacity, storage_max, initial_stock):
    # Create the Gurobi model
    model = Model("Production Planning (Maximizing Profit)")

    # Variables de décision
    x = model.addVars(periods, vtype=GRB.CONTINUOUS, name="Production")  # quantité produite pour chaque période
    s = model.addVars(periods, vtype=GRB.CONTINUOUS, name="Stock")  # qt d=stockée à la fin de chaque période

    # Fonction Objective : Maximiser le profit : (revenue - cout tot de prof et stockage) pour chaque période
    revenue = sum(selling_price[t] * demand[t] for t in periods)
    costs = sum(production_cost[t] * x[t] for t in periods) + sum(storage_cost[t] * s[t] for t in periods)
    model.setObjective(revenue - costs, GRB.MAXIMIZE)

    # Constraints
    #Eq entre prod, stockage et demande pour chaque période
    model.addConstr(s[1] == initial_stock + x[1] - demand[1], "Stock_1")
    for t in periods[1:]:
        model.addConstr(s[t] == s[t-1] + x[t] - demand[t], f"Stock_{t}")

    # qt produite ne dépasse pas la capacité maximale de prod
    for t in periods:
        model.addConstr(x[t] <= capacity[t], f"Capacity_{t}")

    # qt stockée ne dépasse pas la capacité maximale de stock
    for t in periods:
        model.addConstr(s[t] <= storage_max, f"Storage_{t}")

    # les variables doivent etre positives
    for t in periods:
        model.addConstr(x[t] >= 0, f"NonNeg_Production_{t}")
        model.addConstr(s[t] >= 0, f"NonNeg_Storage_{t}")

    # Solve the model
    model.optimize()

    # Check if the solution is optimal
    if model.status == GRB.OPTIMAL:
        results = {
            "Production": {t: x[t].X for t in periods},
            "Stock": {t: s[t].X for t in periods},
            "Profit": model.objVal
        }
        return results
    else:
        raise Exception("No optimal solution found.")

