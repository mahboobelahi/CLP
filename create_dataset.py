"""
This function is used to create the data-set
"""

import json
import random
import boxes as bx

MIN_BOXES = 50
MAX_BOXES = 60
MIN_VALUE = 50
MAX_VALUE = 500
MAX_TRUCK_LEN = 600
MIN_TRUCK_LEN = 300
MAX_TRUCK_WID = 250
MIN_TRUCK_WID = 125
MAX_TRUCK_HT = 250
MIN_TRUCK_HT = 125

truck_dim = [[random.randint(MIN_TRUCK_LEN, MAX_TRUCK_LEN), random.randint(MIN_TRUCK_WID, MAX_TRUCK_WID),
              random.randint(MIN_TRUCK_HT, MAX_TRUCK_HT)] for _ in range(5)]
NUM_BOXES = [
    [random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES),
     random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES)] for _ in range(5)]
dataset = {}
i = 0
for cont, counts in zip(truck_dim, NUM_BOXES):
    for number in counts:
        packages = bx.generateboxes([[0, 0, 0] + cont], number)
        boxes = []
        total_value = 0
        #print(packages)
        for each in packages:
            l, w, h = each[3:]
            vol = l * w * h
            value = random.randint(MIN_VALUE, MAX_VALUE)
            total_value += value
            boxes.append([l, w, h, vol, value])
        dataset[i] = {'truck dimension': [600,250,250], 'number': number, 'boxes': boxes, 'solution': packages,
                      'total value': total_value}
        i += 1

with open('input.json', 'w') as outfile:
    json.dump(dataset, outfile)