import json,time
import random
import visualize_plotly as vis
import visualize as vis2
import population as geni
import fitnesscalc as ft
import recombination as re
import mutation as mt
import nsga2 as ns
import survivor_selection as ss
import matplotlib.pyplot as plt
from tabulate import tabulate
from copy import deepcopy
import matplotlib.tri as mtri
from box import Item
from container import Container
from helper import *

NUM_OF_ITERATIONS = 1
NUM_OF_INDIVIDUALS = 36
NUM_OF_GENERATIONS = 100
output_file = 'truck_and_packages'
PC = int(0.8 * NUM_OF_INDIVIDUALS)
PM1 = 0.2
PM2 = 0.02
K = 2
ROTATIONS = 6  # 1 or 2 or 6
report = {}

# with open('PP_resV2.json', 'w') as json_file:
#     json_file.write((json.dumps(result, indent=4)))

# * ////////////////////////////////////////////////////////////


def plot_stats(average_fitness, title=""):
    x1 = range(len(average_fitness))
    avg_freespace = []
    avg_number = []
    avg_value = []

    for item in average_fitness:
        avg_freespace.append(item[0])
        avg_number.append(item[1])
        avg_value.append(item[2])

    plt.plot(x1, avg_freespace, label='Average Occupied Volume')
    plt.plot(x1, avg_number, label='Average Number of Boxes')
    plt.plot(x1, avg_value, label='Average Value of Boxes')
    plt.xlabel('Number of Generations')
    plt.ylabel('Fitness Values')
    plt.xticks(ticks=[t for t in x1 if t % 20 == 0])
    plt.title(title)
    plt.legend()
    plt.show()


def calc_average_fitness(individuals):
    fitness_sum = [0.0, 0.0, 0.0]
    count = 0
    for key, value in individuals.items():
        if value['Rank'] == 1:
            count += 1
            fitness_sum[0] += value['fitness'][0]
            fitness_sum[1] += value['fitness'][1]
            fitness_sum[2] += value['fitness'][2]
    average = [round(number / count,2) for number in fitness_sum]
    return average


def draw_pareto(population):
    fitness = []
    number = []
    weight = []
    fitness2 = []
    number2 = []
    weight2 = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = []

    for key, value in population.items():
        if value['Rank'] == 1:
            fitness.append(value['fitness'][0])
            number.append(value['fitness'][1])
            weight.append(value['fitness'][2])
            colors.append('red')
        else:
            colors.append('blue')
            fitness2.append(value['fitness'][0])
            number2.append(value['fitness'][1])
            weight2.append(value['fitness'][2])

    if len(fitness) > 2:
        try:
            ax.scatter(fitness2, number2, weight2, c='b', marker='o')
            ax.scatter(fitness, number, weight, c='r', marker='o')
            triang = mtri.Triangulation(fitness, number)
            ax.plot_trisurf(triang, weight, color='red')
            ax.set_xlabel('occupied space')
            ax.set_ylabel('no of boxes')
            ax.set_zlabel('value')
            plt.show()
        except:
            print(
                "ERROR : Please try increasing the number of individuals as the unique Rank 1 solutions is less than 3")


if __name__ == "__main__":
    input_file = 'DataSets/processed/Updated/wtpack1.json'
    with open(input_file, 'r') as outfile:
        data = json.load(outfile)
    problem_indices = list(data.keys())
    boxes = []
    temp_boxes = []
    for p_ind in problem_indices:
        if int(p_ind) >= 1:
            continue
        print("Running Problem Set {}".format(p_ind))
        print(tabulate([['Generations', NUM_OF_GENERATIONS], ['Individuals', NUM_OF_INDIVIDUALS],
                        ['Rotations', ROTATIONS], [
                            'Crossover Prob.', PC], ['Mutation Prob1', PM1],
                        ['Mutation Prob2', PM2], ['Tournament Size', K]], headers=['Parameter', 'Value'],
                       tablefmt="github"))
        print()
        temp_boxes.extend(data[p_ind]["customer1"])
        temp_boxes.extend(data[p_ind]["customer2"])
        temp_boxes.extend(data[p_ind]["customer3"])
        max_weight = 28080
        CONT = Container(
            name=f"ISO-20 feet Dry Container_{p_ind}",
            LWH=data[p_ind]['truck dimension'],
            max_weight=28080
        )
        print(CONT.string())
        # Extracting inputs from the json file
        # * instentiating item objects
        for i in range(len(temp_boxes)):
            box = temp_boxes[i]
            boxes.append(Item(
                partno=f"Box-{i+1}",
                name=f"C-{box[-1]}",
                weight=box[3],
                LWH=box[0:3],
                rotation=0,
                value=box[4]
            ))
        CONT.items.extend(boxes)
        # packages = data[p_ind]['solution']

        # boxes = sorted(boxes, key=lambda xx: xx[5])
        # boxes = random.sample( data[p_ind]['boxes'], 100)
        total_value = sum(i.value for i in boxes)  # data[p_ind]['total value']
        # box_count = data[p_ind]['number']

        box_params = {}
        for index in range(len(boxes)):
            box_params[index] = boxes[index]

        # Storing the average values over every single iteration
        average_vol = []
        average_num = []
        average_value = []
        res = {}
        for i in range(1):
            # Generate the initial population
            population = geni.generate_pop(box_params, NUM_OF_INDIVIDUALS, ROTATIONS)

            gen = 0
            average_fitness = []
            start = time.time()
            while gen < NUM_OF_GENERATIONS:
                print(f"Running current Generations.....{gen}")
                population, fitness = ft.evaluate(population, CONT, box_params, total_value)
                population = ns.rank(population, fitness)
                offsprings = re.crossover(deepcopy(population), PC, k=K)
                offsprings = mt.mutate(offsprings, PM1, PM2, ROTATIONS)
                population = ss.select(population, offsprings, CONT, box_params, total_value,
                                       NUM_OF_INDIVIDUALS)
                average_fitness.append(calc_average_fitness(population))
                #print(f"Running current Generations.....{gen}")
                gen += 1
            end = time.time()
            print(end - start)
            results = []
            customers = {}
            counter = 1
            result = {"cargo_metadata": {
                "container_dimension": [CONT.get_dimention()],
                "container_weight": 28080,
                "container_volume": CONT.get_volume(),
                "total_items": len(CONT.items),
                "packed_items": len(CONT.fit_items),
                "unpacked_items": {"qunatity": len(CONT.unfitted_items),
                                   "item_ids": len([i.get_id() == False for i in CONT.unfitted_items])},
                "consignment_origin": ["City ABC"],
                "consignment_destinations": ["ABC", "ABC", "ABC"]
            }}
            # Storing the final Rank 1 solutions
            for key, value in population.items():
                if value['Rank'] == 1:
                    generate_report(result, value, p_ind, key)
                    # results.append([res.get_plot_data() for res in value['result']])
                    # problem_set[p_ind] = {
                    #         f"result{p_ind}_{key}" : {
                    #         "res":value['result'],
                    #         "fitness":value["fitness"],
                    #         "num":len(value['result'])}
                    #         }
                    # "fitness": ["Vol_utilization(float)", "packed boxes", "Average_Value"],

                # res[f"{p_ind}{key}"] = {
                #     "fitness": value["fitness"],
                #     "num": len(value['result']),
                #     "res": customers
                # }

                # customers[f"customer_{counter}"] = [
                #     customer for customer in value['result'] if customer[-1] in {1}]
                # customers[f"num_C{counter}"] = len(
                #     customers[f"customer_{counter}"])
                # counter += 1
                # customers[f"customer_{counter}"] = [
                #     customer for customer in value['result'] if customer[-1] in {2}]
                # customers[f"num_C{counter}"] = len(
                #     customers[f"customer_{counter}"])
                # counter += 1
                # customers[f"customer_{counter}"] = [
                #     customer for customer in value['result'] if customer[-1] in {3}]
                # customers[f"num_C{counter}"] = len(
                #     customers[f"customer_{counter}"])
                # counter = 1

            # Convert the list to JSON
            json_data = json.dumps(result, indent=2)

            # Save the JSON data to a file
            with open(f'{output_file}.json', 'w') as json_file:
                json_file.write(json_data)
            # Plot using plotly
            # color_index = vis.draw_solution(pieces=packages)
            # vis.draw(results, color_index)

            # Plot using matplotlib
            # x_ticks = 600
            # y_ticks = 250
            # z_ticks = 250
            # step_size = 50
            # # color_index = vis2.draw(x_ticks, y_ticks, z_ticks, step_size,pieces=packages, title="True Solution Packing")
            # j = 0
            # for each in results:
            #     vis2.plot_3d_rectangle(
            #         each, x_ticks, y_ticks, z_ticks, step_size, j+1)
            #     j += 1
            #     # break
            # # for each in results:
            # #     vis2.draw( x_ticks, y_ticks, z_ticks, step_size,each, color_index,title="Rank 1 Solution Packing For Iteration {}".format(i))
            # draw_pareto(population)
            average_vol.append(average_fitness[-1][0])
            average_num.append(average_fitness[-1][1])
            average_value.append(average_fitness[-1][2])
            plot_stats(average_fitness,
                       title="Average Fitness Values for Run {} over {} generations".format(i + 1,
                                                                                            NUM_OF_GENERATIONS))

        print(tabulate(
            [['Problem Set', p_ind], ['Runs', NUM_OF_ITERATIONS], ['Avg. Volume%', sum(average_vol) / len(average_vol)],
             ['Avg. Number%', sum(average_num) / len(average_num)],
             ['Avg. Value%', sum(average_value) / len(average_value)]],
            headers=['Parameter', 'Value'], tablefmt="github"))
    #input("Press Enter to continue...")
