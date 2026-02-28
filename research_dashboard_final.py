import streamlit as st
import pandas as pd
import time
from sklearn.linear_model import LinearRegression

from backend.ga_optimizer import optimize_instances
from backend.rule_based_optimizer import rule_based_scaling
from backend.cost_model import calculate_cost

FILE_PATH = "data/workload_data.csv"
LOG_FILE = "data/performance_metrics.csv"

STATIC_INSTANCES = 2
INSTANCE_CAPACITY = 70

st.set_page_config(page_title="LiveML-Cloud Research Dashboard", layout="wide")

st.title("🚀 LiveML-Cloud: Intelligent Auto-Scaling Research Dashboard")

st.markdown("---")

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


while True:
    try:
        df = pd.read_csv(FILE_PATH)

        if len(df) < 10:
            st.warning("Waiting for sufficient data...")
            time.sleep(2)
            st.rerun()

        predicted_cpu, predicted_memory = get_prediction(df)

        # GA Optimization
        ga_instances, ga_cost = optimize_instances(predicted_cpu)

        # Rule-Based Scaling
        rule_instances, rule_cost = rule_based_scaling(predicted_cpu, predicted_memory)

        static_cost = calculate_cost(STATIC_INSTANCES)

        ga_cost_reduction = ((static_cost - ga_cost) / static_cost) * 100
        ga_efficiency = (predicted_cpu / (ga_instances * INSTANCE_CAPACITY)) * 100

        # ===================== SUMMARY BOX =====================
        st.subheader("📌 Performance Summary")
        st.info(
            f"GA achieves approximately {round(ga_cost_reduction,2)}% cost reduction "
            f"with {round(ga_efficiency,2)}% resource efficiency under current workload."
        )

        # ===================== METRICS =====================
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Predicted CPU (%)", predicted_cpu)
        col2.metric("Predicted Memory (%)", predicted_memory)
        col3.metric("GA Instances", ga_instances)
        col4.metric("Rule Instances", rule_instances)

        col5, col6, col7 = st.columns(3)
        col5.metric("GA Cost (₹)", ga_cost)
        col6.metric("Rule Cost (₹)", rule_cost)
        col7.metric("Static Cost (₹)", static_cost)

        col8, col9 = st.columns(2)
        col8.metric("GA Cost Reduction (%)", round(ga_cost_reduction, 2))
        col9.metric("GA Efficiency (%)", round(ga_efficiency, 2))

        # ===================== SLA STATUS =====================
        st.subheader("🛡 SLA Status")
        if predicted_cpu > 90 or predicted_memory > 90:
            st.error("❌ SLA VIOLATION RISK")
        else:
            st.success("✅ SLA SAFE")

        # ===================== WORKLOAD GRAPHS =====================
        st.subheader("📈 Live CPU Usage Trend")
        st.line_chart(df["cpu_usage"])

        st.subheader("📈 Live Memory Usage Trend")
        st.line_chart(df["memory_usage"])

        # ===================== COST TREND =====================
        if pd.io.common.file_exists(LOG_FILE):
            log_df = pd.read_csv(LOG_FILE)

            st.subheader("📊 GA vs Rule Cost Trend (Historical)")
            if "ga_cost" in log_df.columns and "rule_cost" in log_df.columns:
                st.line_chart(log_df[["ga_cost", "rule_cost"]])

            st.subheader("📊 GA Cost Reduction Trend")
            if "ga_cost_reduction" in log_df.columns:
                st.line_chart(log_df["ga_cost_reduction"])

            # Download button
            st.download_button(
                label="📥 Download Performance Log",
                data=log_df.to_csv(index=False),
                file_name="performance_metrics.csv",
                mime="text/csv"
            )

        st.markdown("---")
        st.caption("LiveML-Cloud | MSc Intelligent Auto-Scaling Framework")

        time.sleep(5)
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
        time.sleep(3)
        st.rerun()