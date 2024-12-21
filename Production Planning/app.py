import streamlit as st
from optimizer import production_planning_optimizer
import pandas as pd

st.title("Production Planning: Maximizing Profit")

#Input: Number of periods
st.header("Input Data")
num_periods = st.slider("Number of Periods", 1, 10, 3)

#Input: Demands table
st.subheader("Demand for each period")
demand_data = pd.DataFrame(
    {
        "Period": list(range(1, num_periods + 1)),
        "Demand": [80] * num_periods
    }
)
demand_data = st.data_editor(demand_data, key="demand_data", use_container_width=True)

#Input: Selling prices table
st.subheader("Selling Price Data")
selling_price_data = pd.DataFrame(
    {
        "Period": list(range(1, num_periods + 1)),
        "Selling Price": [100] * num_periods
    }
)
selling_price_data = st.data_editor(selling_price_data, key="selling_price_data", use_container_width=True)

#Input: Production Cost table
st.subheader("Production Cost Data")
production_cost_data = pd.DataFrame(
    {
        "Period": list(range(1, num_periods + 1)),
        "Production Cost": [50] * num_periods
    }
)
production_cost_data = st.data_editor(production_cost_data, key="production_cost_data", use_container_width=True)

#Input: Storage Cost table
st.subheader("Storage Cost Data")
storage_cost_data = pd.DataFrame(
    {
        "Period": list(range(1, num_periods + 1)),
        "Storage Cost": [5] * num_periods
    }
)
storage_cost_data = st.data_editor(storage_cost_data, key="storage_cost_data", use_container_width=True)

#Input: Production Capacity table
st.subheader("Production Capacity Data")
capacity_data = pd.DataFrame(
    {
        "Period": list(range(1, num_periods + 1)),
        "Production Capacity": [100] * num_periods
    }
)
capacity_data = st.data_editor(capacity_data, key="capacity_data", use_container_width=True)

# inputs common across all periods
storage_max = st.number_input("Max Storage Capacity", min_value=0, value=50, step=10)
initial_stock = st.number_input("Initial Stock", min_value=0, value=20, step=5)

# Solveur
if st.button("Solve Optimization Problem"):
    try:
        # Extract of data from tables that are edited by user
        periods = list(demand_data["Period"])
        demand = dict(zip(periods, demand_data["Demand"]))
        selling_price = dict(zip(periods, selling_price_data["Selling Price"]))
        production_cost = dict(zip(periods, production_cost_data["Production Cost"]))
        storage_cost = dict(zip(periods, storage_cost_data["Storage Cost"]))
        capacity = dict(zip(periods, capacity_data["Production Capacity"]))

        # Call the optimization function
        results = production_planning_optimizer(
            periods=periods,
            demand=demand,
            selling_price=selling_price,
            production_cost=production_cost,
            storage_cost=storage_cost,
            capacity=capacity,
            storage_max=storage_max,
            initial_stock=initial_stock,
        )

        # Display results
        st.success("Optimal solution found!")
        st.write("Production Plan and Stock Levels:")

        st.write("### Production Plan")
        result_table = pd.DataFrame(
            {
                "Period": periods,
                "Produced": [results["Production"][t] for t in periods],
                "Stock": [results["Stock"][t] for t in periods],
            }
        )
        st.table(result_table)

        st.write(f"**Total Profit:** {results['Profit']:.2f}")

    except Exception as e:
        st.error(str(e))
