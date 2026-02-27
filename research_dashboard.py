import streamlit as st
import pandas as pd
import time
from sklearn.linear_model import LinearRegression
from backend.cost_model import calculate_required_instances, calculate_cost

FILE_PATH = "data/workload_data.csv"

INSTANCE_CAPACITY = 70
STATIC_INSTANCES = 2


def get_prediction(df):
    df = df.tail(20).reset_index(drop=True)
    df["time_index"] = range(len(df))

    X = df[["time_index"]]

    cpu_model = LinearRegression()
    cpu_model.fit(X, df["cpu_usage"])
    next_time = pd.DataFrame([[len(df)]], columns=["time_index"])
    cpu_prediction = cpu_model.predict(next_time)[0]

    mem_model = LinearRegression()
    mem_model.fit(X, df["memory_usage"])
    mem_prediction = mem_model.predict(next_time)[0]

    return round(cpu_prediction, 2), round(mem_prediction, 2)


def calculate_efficiency(predicted_cpu, instances):
    total_capacity = instances * INSTANCE_CAPACITY
    return round((predicted_cpu / total_capacity) * 100, 2)


st.set_page_config(page_title="LiveML-Cloud Research Dashboard", layout="wide")

st.title("🚀 LiveML-Cloud: Real-Time Intelligent Scaling Dashboard")

while True:
    try:
        df = pd.read_csv(FILE_PATH)

        if len(df) < 10:
            st.warning("Waiting for sufficient data...")
            time.sleep(2)
            st.rerun()

        predicted_cpu, predicted_memory = get_prediction(df)

        instances = calculate_required_instances(predicted_cpu)
        dynamic_cost = calculate_cost(instances)
        static_cost = calculate_cost(STATIC_INSTANCES)

        cost_reduction = ((static_cost - dynamic_cost) / static_cost) * 100
        efficiency = calculate_efficiency(predicted_cpu, instances)

        # SLA check
        if predicted_cpu > 90 or predicted_memory > 90:
            sla_status = "❌ SLA VIOLATION"
        else:
            sla_status = "✅ SLA SAFE"

        # ====== Layout ======
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Predicted CPU (%)", predicted_cpu)
        col2.metric("Predicted Memory (%)", predicted_memory)
        col3.metric("Required Instances", instances)
        col4.metric("Efficiency (%)", efficiency)

        col5, col6, col7 = st.columns(3)

        col5.metric("Dynamic Cost (₹/min)", dynamic_cost)
        col6.metric("Static Cost (₹/min)", static_cost)
        col7.metric("Cost Reduction (%)", round(cost_reduction, 2))

        st.subheader("SLA Status")
        if "VIOLATION" in sla_status:
            st.error(sla_status)
        else:
            st.success(sla_status)

        st.subheader("Live CPU Usage Trend")
        st.line_chart(df["cpu_usage"])

        st.subheader("Live Memory Usage Trend")
        st.line_chart(df["memory_usage"])

        time.sleep(5)
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
        time.sleep(3)
        st.rerun()