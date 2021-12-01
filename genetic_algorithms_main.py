import Genetic_Algorithms


def fitness(chromosome_information):
    return sum(chromosome_information)


result = Genetic_Algorithms.get_best_chromosome_set(20, fitness)
print(result)
