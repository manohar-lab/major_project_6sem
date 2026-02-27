import pandas as pd
import time
import csv
from datetime import datetime
from sklearn.linear_model import LinearRegression

from cost_model import calculate_cost
from ga_optimizer import optimize_instances
from rule_based_optimizer import rule_based_scaling


FILE_PATH = "../data/workload_data.csv"
STATIC_INSTANCES = 2
INSTANCE_CAPACITY = 70

sla_violations = 0
total_checks = 0


# ===================== Prediction =====================
def get_prediction():
    try:
        df = pd.read_csv(FILE_PATH)

        if len(df) < 10:
            print("Not enough data yet...")
            return None, None

        df = df.tail(20).reset_index(drop=True)
        df["time_index"] = range(len(df))
        X = df[["time_index"]]

        # CPU Model
        cpu_model = LinearRegression()
        cpu_model.fit(X, df["cpu_usage"])
        next_time = pd.DataFrame([[len(df)]], columns=["time_index"])
        cpu_prediction = cpu_model.predict(next_time)[0]

        # Memory Model
        mem_model = LinearRegression()
        mem_model.fit(X, df["memory_usage"])
        mem_prediction = mem_model.predict(next_time)[0]

        return round(cpu_prediction, 2), round(mem_prediction, 2)

    except Exception as e:
        print("Prediction error:", e)
        return None, None


# ===================== Efficiency =====================
def calculate_efficiency(predicted_cpu, instances):
    total_capacity = instances * INSTANCE_CAPACITY
    return round((predicted_cpu / total_capacity) * 100, 2)


# ===================== Logging =====================
def log_performance(timestamp, cpu, memory,
                    ga_instances, ga_cost, ga_cost_reduction, ga_efficiency,
                    rule_instances, rule_cost, rule_cost_reduction, rule_efficiency):

    file_path = "../data/performance_metrics.csv"

    file_exists = False
    try:
        with open(file_path, "r"):
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "predicted_cpu",
                "predicted_memory",
                "ga_instances",
                "ga_cost",
                "ga_cost_reduction",
                "ga_efficiency",
                "rule_instances",
                "rule_cost",
                "rule_cost_reduction",
                "rule_efficiency"
            ])

        writer.writerow([
            timestamp,
            cpu,
            memory,
            ga_instances,
            ga_cost,
            round(ga_cost_reduction, 2),
            ga_efficiency,
            rule_instances,
            rule_cost,
            round(rule_cost_reduction, 2),
            rule_efficiency
        ])


# ===================== Scaling Decision =====================
def scaling_decision():
    global sla_violations, total_checks

    predicted_cpu, predicted_memory = get_prediction()

    if predicted_cpu is None:
        return

    total_checks += 1

    # ----- GA Optimization -----
    ga_instances, ga_cost = optimize_instances(predicted_cpu)

    # ----- Rule-Based Scaling -----
    rule_instances, rule_cost = rule_based_scaling(predicted_cpu, predicted_memory)

    # ----- Static baseline -----
    static_cost = calculate_cost(STATIC_INSTANCES)

    # ----- Cost reduction -----
    ga_cost_reduction = ((static_cost - ga_cost) / static_cost) * 100
    rule_cost_reduction = ((static_cost - rule_cost) / static_cost) * 100

    # ----- Efficiency -----
    ga_efficiency = calculate_efficiency(predicted_cpu, ga_instances)
    rule_efficiency = calculate_efficiency(predicted_cpu, rule_instances)

    # ----- Logging -----
    log_performance(
        datetime.now(),
        predicted_cpu,
        predicted_memory,
        ga_instances,
        ga_cost,
        ga_cost_reduction,
        ga_efficiency,
        rule_instances,
        rule_cost,
        rule_cost_reduction,
        rule_efficiency
    )

    # ----- Output -----
    print("===================================")
    print(f"Predicted CPU: {predicted_cpu}%")
    print(f"Predicted Memory: {predicted_memory}%")

    print("\n--- GA Optimization ---")
    print(f"Instances: {ga_instances}")
    print(f"Cost: ₹{ga_cost}")
    print(f"Cost Reduction: {round(ga_cost_reduction, 2)}%")
    print(f"Efficiency: {ga_efficiency}%")

    print("\n--- Rule-Based Scaling ---")
    print(f"Instances: {rule_instances}")
    print(f"Cost: ₹{rule_cost}")
    print(f"Cost Reduction: {round(rule_cost_reduction, 2)}%")
    print(f"Efficiency: {rule_efficiency}%")


# ===================== Main Loop =====================
if __name__ == "__main__":
    while True:
        scaling_decision()
        time.sleep(5)