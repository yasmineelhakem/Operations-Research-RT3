import streamlit as st
import pandas as pd
from optimizer import production_planning_optimizer

st.title("Optimisation de la Production pour Plusieurs Produits")
st.header("Données d'entrée")

num_products = st.slider("Nombre de produits", 1, 5, 2)
num_periods = st.slider("Nombre de périodes", 1, 10, 3)

products = [f"Produit {i+1}" for i in range(num_products)]
periods = list(range(1, num_periods + 1))

# Propriétés des produits
properties = {}
for p in products:
    st.subheader(f"Propriétés de {p}")
    properties[p] = {
        "perissable": st.checkbox(f"{p} est périssable"),
        "critique": st.checkbox(f"{p} est critique"),
        "fragile": st.checkbox(f"{p} est fragile"),
    }

# Tableau des données
input_data = pd.DataFrame(
    {
        "Produit": products * num_periods,
        "Période": [p for _ in products for p in periods],
        "Demande": [80] * num_products * num_periods,
        "Prix de vente": [100] * num_products * num_periods,
        "Coût de production": [50] * num_products * num_periods,
        "Coût de stockage": [5] * num_products * num_periods,
        "Capacité de production": [100] * num_products * num_periods,
    }
)
input_data = st.data_editor(input_data, key="input_data", use_container_width=True)
#print(input_data)

storage_max = {p: st.number_input(f"Capacité max de stockage pour {p}", min_value=0, value=50, step=10) for p in products}
initial_stock = {p: st.number_input(f"Stock initial pour {p}", min_value=0, value=20, step=5) for p in products}

if st.button("Résoudre le problème d'optimisation"):
    try:
        demand = {p: dict(zip(periods, input_data[input_data["Produit"] == p]["Demande"])) for p in products}
        selling_price = {p: dict(zip(periods, input_data[input_data["Produit"] == p]["Prix de vente"])) for p in products}
        production_cost = {p: dict(zip(periods, input_data[input_data["Produit"] == p]["Coût de production"])) for p in products}
        storage_cost = {p: dict(zip(periods, input_data[input_data["Produit"] == p]["Coût de stockage"])) for p in products}
        capacity = {p: dict(zip(periods, input_data[input_data["Produit"] == p]["Capacité de production"])) for p in products}

        print("demand",demand)

        results = production_planning_optimizer(
            products=products,
            periods=periods,
            demand=demand,
            selling_price=selling_price,
            production_cost=production_cost,
            storage_cost=storage_cost,
            capacity=capacity,
            storage_max=storage_max,
            initial_stock=initial_stock,
            properties=properties,
        )

        st.success("Solution optimale trouvée!")
        st.write("### Résultats par produit")
        for p in products:
            st.write(f"#### {p}")
            result_table = pd.DataFrame(
                {
                    "Période": periods,
                    "Production": [results["Production"][p][t] for t in periods],
                    "Stock": [results["Stock"][p][t] for t in periods],
                }
            )
            st.table(result_table)
        st.write(f"**Profit total :** {results['Profit']:.2f}")

    except Exception as e:
        st.error(f"Erreur: {str(e)}")
