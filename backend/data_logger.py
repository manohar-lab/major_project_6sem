import csv
import os
import time
from workload_simulator import generate_workload

FILE_PATH = "../data/workload_data.csv"

def initialize_file():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "cpu_usage", "memory_usage"])

def log_data():
    initialize_file()
    while True:
        data = generate_workload()
        with open(FILE_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                data["timestamp"],
                data["cpu_usage"],
                data["memory_usage"]
            ])
        print("Logged:", data)
        time.sleep(2)

if __name__ == "__main__":
    log_data()