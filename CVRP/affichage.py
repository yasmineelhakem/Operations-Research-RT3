# Input list of tuples representing directed edges
route = [(0, 2), (0, 3), (2, 0), (3, 4), (4, 5), (5, 0)]

def affichage(route):
    e = 0
    chain = []

    while route:
        found = False
        for i, edge in enumerate(route):
            if edge[0] == e:
                chain.append(e)
                e = edge[1]
                route.pop(i)
                found = True
                break
        if not found:
            print("No valid route can be formed.")
            break

    chain.append(e)
    return "->".join(map(str, chain))
print(affichage(route))
