from backend.cost_model import calculate_required_instances, calculate_cost


def rule_based_scaling(predicted_cpu, predicted_memory):

    if predicted_cpu > 70 or predicted_memory > 75:
        instances = calculate_required_instances(predicted_cpu)
    elif predicted_cpu < 40 and predicted_memory < 40:
        instances = 1
    else:
        instances = 1

    cost = calculate_cost(instances)

    return instances, cost