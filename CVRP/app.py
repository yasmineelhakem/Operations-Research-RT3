import streamlit as st
import numpy as np
from optimizer import solve_cvrp
import pandas as pd
from affichage import affichage

st.markdown(
    """
    <h1 style='text-align: center; color: white; font: serif;'>
        Capacitated Vehicle Routing Problem 
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

# Demand of each client
st.subheader("Enter demands for each client:")
d = [0]
for i in range(1,N):
    d.append(st.number_input(f"Demand for client {i}:", min_value=0, value=0 if i == 0 else 1))

# Distance matrix
st.subheader("Enter the values for the distance matrix:")

initial_matrix = pd.DataFrame(
    np.zeros((N, N)),
    columns=[f"Client {i}" for i in range(N)],
    index=[f"Client {i}" for i in range(N)]
)

for i in range(N):
    for j in range(N):
        if  i>=j:
            initial_matrix.iloc[i, j] = np.nan

edited_matrix = st.data_editor(initial_matrix)

df = pd.DataFrame(
    np.zeros((N, N)),
    columns=[f"Client {i}" for i in range(N)],
    index=[f"Client {i}" for i in range(N)],
)

for i in range(N):
    for j in range(N):
        if i>j:
            df.iloc[i, j] = edited_matrix.iloc[j, i]
        elif i<j:
            df.iloc[i, j] = edited_matrix.iloc[i, j]
        else:
            df.iloc[i, j] = 0.0

D = np.array(df)
print(df)
print(D)

#np.fill_diagonal(D, 0)

if st.button("Solve CVRP"):
    result = solve_cvrp(N, Q, K, d, D)
    if result["status"] == "Optimal":
        st.success("Optimal solution found!")
        st.write(f"Total travel distance: {result['total_distance']}")
        for k, route in result["routes"].items():
            st.write(f"Vehicle {k + 1}:")
            #st.write("then ".join(f"{i} to {j} " for i, j in route))
            if route :
                st.write(affichage(route))
            else:
                st.write(f"Vehicule number {k +1 } is not needed")
    else:
        st.error(result["status"])
