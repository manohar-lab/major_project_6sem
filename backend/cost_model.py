def calculate_required_instances(predicted_cpu):
    # Each instance can handle 70% CPU safely
    capacity_per_instance = 70

    instances = max(1, int(predicted_cpu // capacity_per_instance) + 1)
    return instances


def calculate_cost(instances):
    cost_per_instance = 2  # ₹2 per minute
    return instances * cost_per_instance


if __name__ == "__main__":
    test_cpu = 85
    instances = calculate_required_instances(test_cpu)
    cost = calculate_cost(instances)

    print(f"Predicted CPU: {test_cpu}")
    print(f"Required Instances: {instances}")
    print(f"Estimated Cost per minute: ₹{cost}")