import streamlit as st
import numpy as np
from cvrp_optimizer import solve_cvrp
import pandas as pd

#st.title("Capacitated Vehicle Routing Problem (CVRP) Solver")
st.markdown(
    """
    <h1 style='text-align: center; color: white; font: serif;'>
        Capacitated Vehicle Routing Problem (CVRP) Solver
    </h1>
    """,
    unsafe_allow_html=True
)

# Number of clients (including depot)
N = st.number_input("Enter the number of clients (including depot):", min_value=1, value=3, step=1)

# Vehicle capacity
Q = st.number_input("Enter vehicle capacity:", min_value=1, value=15)

# Number of vehicles
K = st.number_input("Enter the number of vehicles:", min_value=1, value=2, step=1)

# Demands of each client
st.subheader("Enter demands for each client (including depot as 0):")
d = []
for i in range(N):
    d.append(st.number_input(f"Demand for client {i}:", min_value=0, value=0 if i == 0 else 1))

# Distance matrix
initial_matrix = pd.DataFrame(
    np.zeros((N, N)),
    columns=[f"Client {i}" for i in range(N)],
    index=[f"Client {i}" for i in range(N)]
)

# THe matrix must be edited by the user
st.subheader("Enter the values for the distance matrix:")
edited_matrix = st.data_editor(initial_matrix, num_rows="dynamic")

D = np.array(edited_matrix)

# Diagonal lezem tkoun 0 (distance between client 0 and client 0)
np.fill_diagonal(D, 0)

# Solve
if st.button("Solve CVRP"):
    result = solve_cvrp(N, Q, K, d, D)
    if result["status"] == "Optimal":
        st.success("Optimal solution found!")
        st.write(f"Total travel distance: {result['total_distance']}")
        for k, route in result["routes"].items():
            st.write(f"Vehicle {k + 1}:")
            st.write(" -> ".join(f"{i} to {j}" for i, j in route))
    else:
        st.error(result["status"])
