import pandas as pd
import time
from sklearn.linear_model import LinearRegression

FILE_PATH = "../data/workload_data.csv"

def train_and_predict():
    try:
        df = pd.read_csv(FILE_PATH)

        # Convert timestamp to numerical index
        df["time_index"] = range(len(df))

        # Feature & Target
        X = df[["time_index"]]
        y = df["cpu_usage"]

        model = LinearRegression()
        model.fit(X, y)

        next_time = [[len(df)]]
        prediction = model.predict(next_time)

        print(f"Predicted Next CPU Usage: {round(prediction[0],2)}")

    except Exception as e:
        print("Waiting for enough data...", e)

if __name__ == "__main__":
    while True:
        train_and_predict()
        time.sleep(5)