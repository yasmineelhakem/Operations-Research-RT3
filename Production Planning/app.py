import streamlit as st
from optimizer import production_planning_optimizer
import pandas as pd

st.title("Production Planning: Maximizing Profit")
st.header("Input Data")
num_periods = st.slider("Number of Periods", 1, 10, 3)

input_data = pd.DataFrame(
    {
        "Period": list(range(1, num_periods + 1)),
        "Demand": [80] * num_periods,
        "Selling Price": [100] * num_periods,
        "Production Cost": [50] * num_periods,
        "Storage Cost": [5] * num_periods,
        "Production Capacity": [100] * num_periods,
    }
)

input_data = st.data_editor(input_data, key="input_data", use_container_width=True)

storage_max = st.number_input("Max Storage Capacity", min_value=0, value=50, step=10)
initial_stock = st.number_input("Initial Stock", min_value=0, value=20, step=5)

if st.button("Solve Optimization Problem"):
    try:
        # Extract data from the single table
        periods = list(input_data["Period"])
        demand = dict(zip(periods, input_data["Demand"]))
        selling_price = dict(zip(periods, input_data["Selling Price"]))
        production_cost = dict(zip(periods, input_data["Production Cost"]))
        storage_cost = dict(zip(periods, input_data["Storage Cost"]))
        capacity = dict(zip(periods, input_data["Production Capacity"]))

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
