from gurobipy import Model, GRB

def production_planning_optimizer(products, periods, demand, selling_price, production_cost, storage_cost, capacity, storage_max, initial_stock, properties):
    model = Model("Production Planning (Multi-Product)")

    # Variables de décision
    x = model.addVars(products, periods, vtype=GRB.CONTINUOUS, name="Production")
    s = model.addVars(products, periods, vtype=GRB.CONTINUOUS, name="Stock")

    # Fonction objective : Maximiser le profit
    revenue = sum(selling_price[p][t] * demand[p][t] for p in products for t in periods)
    costs = sum(production_cost[p][t] * x[p, t] for p in products for t in periods) + sum(storage_cost[p][t] * s[p, t] for p in products for t in periods)
    model.setObjective(revenue - costs, GRB.MAXIMIZE)

    # Contraintes
    for p in products:
        # Contraintes de balance production-stock-demande
        model.addConstr(s[p, 1] == initial_stock[p] + x[p, 1] - demand[p][1], f"Stock_{p}_1")
        for t in periods[1:]:
            model.addConstr(s[p, t] == s[p, t - 1] + x[p, t] - demand[p][t], f"Stock_{p}_{t}")

        # Limites de production et stockage
        for t in periods:
            model.addConstr(x[p, t] <= capacity[p][t], f"Capacity_{p}_{t}")
            model.addConstr(s[p, t] <= storage_max[p], f"Storage_{p}_{t}")
            model.addConstr(x[p, t] >= 0, f"NonNeg_Production_{p}_{t}")
            model.addConstr(s[p, t] >= 0, f"NonNeg_Storage_{p}_{t}")

        # Produits critiques : stock minimum (il ne faut pas avoir stock ==0 )
        if properties[p]["critique"]:
            for t in periods:
                model.addConstr(s[p, t] >= 10, f"Critique_{p}_{t}")  # Exemple : stock minimum = 10

        # Produits périssables : stock doit être consommé rapidement ( produits alilentaires par exemples)
        if properties[p]["perissable"]:
            for t in periods:
                if t + 1 in periods:
                    model.addConstr(s[p, t + 1] <= 0.5 * s[p, t], f"Perissable_{p}_{t}")

        # Produits fragiles : stockage n'est pas le stockage maximal
        if properties[p]["fragile"]:
            for t in periods:
                model.addConstr(s[p, t] <= 0.8 * storage_max[p], f"Fragile_{p}_{t}")  # Exemple : 20% de stockage max en moins

    model.optimize()

    if model.status == GRB.OPTIMAL:
        results = {
            "Production": {p: {t: x[p, t].X for t in periods} for p in products},
            "Stock": {p: {t: s[p, t].X for t in periods} for p in products},
            "Profit": model.objVal,
        }
        return results
    else:
        raise Exception("No optimal solution found.")
