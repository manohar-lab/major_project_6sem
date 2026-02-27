import random
import time
from datetime import datetime

def generate_workload():
    cpu = random.uniform(20, 90)
    memory = random.uniform(30, 95)
    return {
        "timestamp": datetime.now(),
        "cpu_usage": round(cpu, 2),
        "memory_usage": round(memory, 2)
    }

if __name__ == "__main__":
    while True:
        data = generate_workload()
        print(data)
        time.sleep(2)