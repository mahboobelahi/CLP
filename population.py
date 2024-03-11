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
        # *sort by length,width,height,Vol,Value in decreasing

    for i in range(0, 5):
        if i == 4:
            sorted_box = dict(
                sorted(box_params.items(),
                       # Call the method to get the volume
                       key=lambda xx: xx[1].get_volume(),
                       reverse=True))
        else:
            sorted_box = dict(
                sorted(box_params.items(),
                       # Use getattr for other attributes
                       key=lambda xx: getattr(
                           xx[1], ['length', 'width', 'height','value'][i]),
                       reverse=True))

        population[i] = {"order": list(sorted_box.keys()),
                         "rotate": [random.randint(0, rotation - 1) for r in range(len(box_params))],

                         }
        # print("///////////////")
        # for  k,v in sorted_box.items():
        #         pprint((k,v.get_volume(), v.get_dimention()))
        # print("///////////////")
    keys = list(box_params.keys())
    for i in range(5, count):
        random.shuffle(keys)
        population[i] = {"order": deepcopy(keys),
                         "rotate": [random.randint(0, rotation - 1) for r in range(len(box_params))]}
        # boxes=sorted(boxes,key=lambda item: (item.get_volume(),item.get_dimention()[0]),reverse=True)#,item[2],item[1]
        # boxes=sorted(boxes,key=lambda item: (item.get_id().split("C-")[1]),reverse=False)
        # from pprint import pprint
        # pprint([(i.get_volume(),i.get_dimention()) for i in boxes])
    return population
