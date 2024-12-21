import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

def plot_fig(D, path):
    # place the points on the figure according the distance matrix between clients
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    positions = mds.fit_transform(D)

    plt.figure(figsize=(8, 6))
    plt.scatter(positions[:, 0], positions[:, 1], marker='o', color='b')
    plt.scatter(positions[0, 0], positions[0, 1], color='red', edgecolor='white', s=200, linewidth=2, zorder=5) # the depot

    # Draw pathes
    for i in range(len(path) - 1):
        point_a = positions[path[i]]
        point_b = positions[path[i + 1]]
        plt.plot([point_a[0], point_b[0]], [point_a[1], point_b[1]], color='r', linestyle='-', linewidth=2)
        midpath = [(point_a[0] + point_b[0]) / 2, (point_a[1] + point_b[1]) / 2] # mid of the path where to place the number
        plt.text(midpath[0], midpath[1], f'{i + 1}', color='black', fontsize=12, ha='center', va='center')

    for i, pos in enumerate(positions):
        if i == 0:
            plt.text(pos[0] , pos[1], "Depot", color='black', fontsize=12)
        else:
            plt.text(pos[0], pos[1], "Client "+str(i), color='black', fontsize=12)

    plt.title('Path of the vehicle ')
    plt.xlabel('X ')
    plt.ylabel('Y ')
    plt.grid(True)

    return plt.gcf()

distance_matrix = np.array([
    [0, 2, 3, 4],
    [2, 0, 1, 3],
    [3, 1, 0, 2],
    [4, 3, 2, 0]
])

order = [0, 1, 2, 3, 0]

# Plot the figure and show it
fig = plot_fig(distance_matrix, order)
plt.show()
