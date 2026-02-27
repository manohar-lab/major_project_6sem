import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = "data/performance_metrics.csv"

def analyze():
    df = pd.read_csv(FILE_PATH)

    print("========= EXPERIMENTAL RESULTS =========")
    print(f"Total Observations: {df.shape[0]}")
    print(f"Average Cost Reduction: {round(df['cost_reduction_percent'].mean(),2)}%")
    print(f"Average Efficiency: {round(df['efficiency_percent'].mean(),2)}%")
    print("=========================================")

    # -------- Graph 1: Cost Comparison --------
    plt.figure()
    plt.plot(df["dynamic_cost"], label="Dynamic Cost")
    plt.plot(df["static_cost"], label="Static Cost")
    plt.title("Dynamic vs Static Cost")
    plt.legend()
    plt.xlabel("Time Step")
    plt.ylabel("Cost (₹)")
    plt.show()

    # -------- Graph 2: Cost Reduction Trend --------
    plt.figure()
    plt.plot(df["cost_reduction_percent"])
    plt.title("Cost Reduction Percentage Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Cost Reduction (%)")
    plt.show()

    # -------- Graph 3: Efficiency Trend --------
    plt.figure()
    plt.plot(df["efficiency_percent"])
    plt.title("Resource Utilization Efficiency Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Efficiency (%)")
    plt.show()

    # -------- Graph 4: Instances Used --------
    plt.figure()
    plt.plot(df["instances"])
    plt.title("Instances Selected by GA Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Instances")
    plt.show()


if __name__ == "__main__":
    analyze()