import pygad
from cost_model import calculate_cost

INSTANCE_CAPACITY = 70


def optimize_instances(predicted_cpu):

    def fitness_func(ga_instance, solution, solution_idx):
        instances = int(solution[0])

        if instances <= 0:
            return -999999

        cpu_per_instance = predicted_cpu / instances
        cost = calculate_cost(instances)

        # Hard SLA constraint
        if cpu_per_instance > INSTANCE_CAPACITY:
            return -100000

        # Efficiency calculation
        efficiency = (predicted_cpu / (instances * INSTANCE_CAPACITY)) * 100

        # Strong cost minimization + efficiency reward
        fitness = (efficiency * 2) - (cost * 15)

        return fitness

    ga_instance = pygad.GA(
        num_generations=30,
        num_parents_mating=4,
        fitness_func=fitness_func,
        sol_per_pop=10,
        num_genes=1,
        gene_type=int,
        gene_space=[1, 2, 3, 4, 5],
        parent_selection_type="sss",
        keep_parents=1,
        crossover_type="single_point",
        mutation_type="random",
        mutation_num_genes=1
    )

    ga_instance.run()

    solution, solution_fitness, _ = ga_instance.best_solution()

    optimal_instances = int(solution[0])
    optimal_cost = calculate_cost(optimal_instances)

    return optimal_instances, optimal_cost