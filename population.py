import random
from copy import deepcopy
from pprint import pprint

def generate_pop(box_params, count, rotation=5):
    """
    This function uses the dimensions of the boxes to create a diploid chromosome for every individual in the population,
    It consists of 'order', which is a permutation as the boxes order and a list of their rotation values
    :param box_params: A dictionary of the box number as the key and a list of [l, w, h, vol, value] of the boxes as values
    :param count: Number of individuals in a population
    :param rotation: Value of the degrees of rotation allowed
    :return: A dictionary of individuals, with order, rotate and values for each box
    """
    population = {}
    if count > 5:
        x = 5
    else:
        x = count
    print(box_params)
    for i in range(0, x):
        #*sort by length,width,height,Vol,Value
        sorted_box = dict(sorted(box_params.items(), key=lambda xx: xx[1][i]))
        print(sorted_box)
        #! add constraints like Stack,priority,zone, weight, load balancing etc to population
        population[i] = {"order": list(sorted_box.keys()),
                         "rotate": [random.randint(0, rotation - 1) for r in range(len(box_params))]}

    keys = list(box_params.keys())
    for i in range(5, count):
        random.shuffle(keys)
        population[i] = {"order": deepcopy(keys),
                         "rotate": [random.randint(0, rotation - 1) for r in range(len(box_params))]}
    return population
