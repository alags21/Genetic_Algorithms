import random
import math

# chromosome class
# Methods - Child of chromosomes (self, other) =D
# Mutation Method - randomly switch a few alleles =D

# External Functions
# STARTING POINT : take chromosome length_of_chrom ([1, 0, 1] = 3), and two very different =D
# reproduce
# In between iterations : delete percentage of worst chromosomes
# End check function : check |fitness - previous fitness)| < some ratio

class Chromosome:
    def __init__(self, items, fitness_function):
        self.items = items
        self.length = len(self.items)
        self.fitness = fitness_function(self.items)
        self.fitness_function = fitness_function

    def child(self, parent2):
        child_list = []
        for allele_position in range(0, self.length):
             random_num = random.randint(0, 1)
             if random_num == 0:
                 child_list.append(self.items[allele_position])
             else:
                 child_list.append(parent2.items[allele_position])

        child_chromsome = Chromosome(child_list, self.fitness_function)
        return child_chromsome.mutate()

    def mutate(self):
        mutation_threshold = 2
        if self.length >= mutation_threshold:
            random_allele = random.randint(0, self.length - 1)
            if self.items[random_allele] == 0:
                self.items[random_allele] = 1
            else:
                self.items[random_allele] = 0

        return self

    def __str__(self):
        return str(self.items)

    def __repr__(self):
        return str(self.items)

def get_best_chromosome_set(length, fitness_function):
    chromosomes = []

    new_chrom_items = []
    for l in range(length):
        new_chrom_items.append(0)

    chromosomes.append(Chromosome(new_chrom_items, fitness_function))

    new_chrom_items = []
    ind = 0
    for combo in range(length):
        for allele in range(length):
            if ind == allele:
                new_chrom_items.append(1)
            else:
                new_chrom_items.append(0)

        ind += 1
        chromosomes.append(Chromosome(new_chrom_items, fitness_function))
        new_chrom_items = []

    if len(chromosomes) % 2 == 1:
        new_chrom_items = []
        for l in range(length):
            new_chrom_items.append(1)

        chromosomes.append(Chromosome(new_chrom_items, fitness_function))

    return iteration(chromosomes, length, None)

def check_if_viable_parent(p1, p2, used):
    if p1 == p2:
        return False
    elif p1 in used:
        return False
    elif p2 in used:
        return False
    else:
        return True


def iteration(chromosome_list, length_of_chrom, prev_chrom_set):
    used_chroms = []
    all_chroms = chromosome_list
    parent_chroms = chromosome_list
    chrom_list_len = int(len(chromosome_list))

    for pair in range(0, chrom_list_len):
        parent1_ind = random.randint(0, chrom_list_len - 1)
        parent2_ind = random.randint(0, chrom_list_len - 1)

        while check_if_viable_parent(parent1_ind, parent2_ind, used_chroms):
            parent1_ind = random.randint(0, chrom_list_len - 1)
            parent2_ind = random.randint(0, chrom_list_len - 1)

        parent1 = parent_chroms[parent1_ind]
        parent2 = parent_chroms[parent2_ind]
        child = parent1.child(parent2)
        used_chroms.append(parent1_ind)
        used_chroms.append(parent2_ind)
        all_chroms.append(child)

    final_chrom_for_round = low_fitness_removal(all_chroms)

    if prev_chrom_set == None:
        return iteration(final_chrom_for_round, length_of_chrom, final_chrom_for_round)

    else:
       return best_fit_check(final_chrom_for_round, prev_chrom_set)


def low_fitness_removal(list_of_chroms):

    num_to_be_removed = math.ceil(len(list_of_chroms)/2)
    num_removed = 0

    ordered_chroms = []

    for to_be_ordered_chromosome in list_of_chroms:

        if ordered_chroms == []:
            ordered_chroms.append([to_be_ordered_chromosome])

        else:
            ordered_chroms.append(ordered_chroms[-1])
            is_greatest = False
            for ind, already_in_the_list_chromosome in enumerate(ordered_chroms[-1]):
                if to_be_ordered_chromosome.fitness < already_in_the_list_chromosome.fitness:
                    ordered_chroms[-1].insert(ind, to_be_ordered_chromosome)
                    is_greatest = True
                    break

            if is_greatest == False:
                ordered_chroms[-1].append(to_be_ordered_chromosome)

    most_fit_chroms = ordered_chroms[-1][num_to_be_removed:]
    return most_fit_chroms

def best_fit_check(current_chrom_set, previous_chrom_set):
    current_average = 0
    current_num_of_chroms = 0

    for allele in current_chrom_set:
        current_num_of_chroms += 1
        current_average += allele.fitness

    current_average /= current_num_of_chroms

    previous_average = 0
    previous_num_of_chroms = 0

    for alele in previous_chrom_set:
        previous_average += alele.fitness
        previous_num_of_chroms += 1

    previous_average /= previous_num_of_chroms

    if abs(current_average - previous_average) / current_average < 0.02:
        return current_chrom_set

    else:
        return iteration(current_chrom_set, int(len(current_chrom_set[0].items)), current_chrom_set)
