import copy
from operator import itemgetter
from copy import deepcopy
from pprint import pprint
from helper import *
import visualize as vis2
import json


def evaluate(population, CONT, boxes_objs, total_value, support_ratio=0.70):
    """
    This function uses the S-DBLF algorithm to pack the boxes in the container and calculates the utilization space, the
    number of boxes packed and the total value of the boxes packed onto the container as the fitness values
    :param population: A dictionary of individuals, with order, rotate and values for each box
    :param truck_dimension: The [l, w, h] of the container
    :param boxes: A dictionary of the box number as the key and a list of [l, w, h, vol, value] of the boxes as values
    :return: The population dictionary adn list of fitness values for every individual
    """
    L, W, H = CONT.get_dimention()
    ft = {}

    for key, individual in population.items():

        print(f"processing key.....{key}")
        occupied_vol = 0
        number_boxes = 0
        value = 0
        result = []
        # copying placement points a list [[0,0,0]]
        PP = copy.deepcopy(CONT.PP)
        # * boxes =  copy.deepcopy(boxes_objs)
        items = [(copy.deepcopy(boxes_objs)[box_number], r)
                 for box_number, r in zip(individual['order'], individual['rotate'])]
        
        boxes = sorted(items, key=lambda item: (-item[0].get_volume(), item[1]))
        # boxes = sorted(items, key=lambda item: (item[0].get_volume(), item[0].get_dimention()[0]), reverse=True)  # ,item[2],item[1]
        # boxes = sorted(boxes, key=lambda item: (item[0].get_id().split("C-")[1]), reverse=False)
        # for  v,r in boxes:
        #         pprint((v.get_volume(), v.get_dimention()))
        for box, r in boxes[:]:
            box.rotation_type = r
            l, w, h = box.get_dimention()

            for pos in PP[:]:
                is_overlap = []
                support_area = []
                is_hanging = []
                temp = {}
                temp_pp = []
                if pos == [0, 0, 0]:  # first box in container
                    box.set_onBase(True)
                    box.set_position(pos)
                    box.is_fit = True
                    CONT.fit_items.append(box)
                    # occupied_vol += box.get_volume()
                    # number_boxes += 1
                    # value += box.value
                    temp_pp = []
                    if pos[0]+l < L:
                        temp_pp.append([pos[0]+l, pos[1], pos[2]])
                    if pos[1]+w < W:
                        temp_pp.append([pos[0], pos[1]+w, pos[2]])
                    if pos[2]+h < H:
                        temp_pp.append([pos[0], pos[1], pos[2]+h])

                    PP.remove(pos)
                    # boxes.remove((box, r))
                    # best_point.extend([pos])
                    PP.extend(temp_pp)
                    box.set_pps(temp_pp)
                    PP = sorted(PP, key=lambda point: (point[0], point[2], point[1]), reverse=False)
                    break

                if (L < pos[0]+l or W < pos[1]+w or H < pos[2]+h):
                    continue
                for current_item in CONT.fit_items:  # iterate over items placed in container

                    box1 = current_item.get_position()+current_item.get_dimention()
                    box2 = pos+box.get_dimention()
                    current_item.set_allvertices(current_item.get_position()+current_item.get_dimention())
                    box.set_allvertices(pos+box.get_dimention())
                    box1_vertices = current_item.get_allVertices()
                    box2_vertices = box.get_allVertices()
                    check_overlap = intersect(box1, box2)
                    is_overlap.append(check_overlap)
                    # here i am making box neighbours
                    if (box1_vertices["FTL"] == box2_vertices["FBL"]) and check_overlap == False:
                        if box1 not in box.under:
                            box.under.append([current_item, calculate_overlap_area(box1, box2)])
                            current_item.top.append([box, calculate_overlap_area(box1, box2)])

                    if (box1_vertices["BBL"] == box2_vertices["FBL"]) and check_overlap == False:
                        current_item.besideR.append(box)
                        box.besideL.append(current_item)

                    if (box1_vertices["FBR"] == box2_vertices["FBL"]) and check_overlap == False:
                        current_item.front.append(box)
                        box.back.append(current_item)

                if True in is_overlap:
                    clear_neighbors(current_item, box)
                    continue

                obj = None
                area = 0
                # *case1
                if box.under and pos[2] != 0:
                    obj, _ = box.get_under()[0]
                    area += calculate_overlap_area(obj.get_position()+obj.get_dimention(),
                                                   pos+box.get_dimention())
                    if area < support_ratio:
                        clear_neighbors(current_item, box)
                        continue
                    else:
                        if obj.besideR:
                            if obj.besideR[0].top:
                                top_boxes = get_top_boxes(obj.besideR[0].top)
                                if (box.get_dimention()[2]/top_boxes[-1].get_dimention()[2]) > support_ratio:
                                    area3 = calculate_overlap_area(top_boxes[-1].get_position() + top_boxes[-1].get_dimention(),
                                                                   pos + box.get_dimention())
                                    box.under.append([top_boxes[-1], area3])
                                    top_boxes[-1].top.append([box, area3])
                            else:
                                area3 = calculate_overlap_area(obj.besideR[0].get_position()+obj.get_dimention(),
                                                               pos+box.get_dimention())
                                if area3 > 0:
                                    box.under.append([obj.besideR[0], area3])
                                    obj.besideR[0].top.append([box, area3])
                # *case2
                elif box.back and pos[2] != 0:
                    if box.back[0].get_under():
                        obj, _ = box.back[0].get_under()[0]
                        area += calculate_overlap_area(obj.get_position()+obj.get_dimention(),
                                                       pos+box.get_dimention())
                        if area < support_ratio:
                            # remove_pp(area,CONT,removed_PP,pos)
                            clear_neighbors(current_item, box)
                            continue
                        else:
                            area3 = 0
                            box.under.append([obj, area])
                            obj.top.append([box, area])
                            if obj.besideR:
                                area3 += calculate_overlap_area(obj.besideR[0].get_position()+obj.besideR[0].get_dimention(),
                                                                pos+box.get_dimention())
                                if area3 > 0:
                                    box.under.append([obj.besideR[0], area3])
                                    obj.besideR[0].top.append([box, area3])
                # *case3:
                elif box.besideL and pos[2] != 0:
                    if box.besideL[0].get_under():
                        area1 = 0
                        under_boxes = box.besideL[0].get_under()
                        # if len(under_boxes) >= 3:
                        for b in under_boxes:
                            area1 = calculate_overlap_area(b[0].get_position() + b[0].get_dimention(),
                                                           pos + box.get_dimention())
                            if area1 > 0:
                                obj, _ = b
                                break

                        area2 = 0
                        if area1 < .5 and obj != None:
                            if obj.besideR:
                                area2 += calculate_overlap_area(obj.besideR[0].get_position()+obj.besideR[0].get_dimention(),
                                                                pos+box.get_dimention())

                        area = area1+area2

                        if area1 != 0 and area1 > 0.7:
                            area3 = 0
                            box.under.append([obj, area1])
                            obj.top.append([box, area1])
                            if obj.besideR and calculate_overlap_area(obj.besideR[0].get_position()+obj.besideR[0].get_dimention(),
                                                                      pos+box.get_dimention()) > 0:
                                area3 = calculate_overlap_area(obj.besideR[0].get_position()+obj.besideR[0].get_dimention(),
                                                               pos+box.get_dimention())
                                box.under.append([obj.besideR[0], area3])
                                obj.besideR[0].top.append([box, area3])
                        if area2 != 0 and area2 > 0.7:
                            box.under.append([obj.besideR[0], area2])
                            obj.besideR[0].top.append([box, area2])

                    if area < support_ratio:
                        clear_neighbors(current_item, box)
                        continue
                else:
                    pass

                fit = True
                # print(CONT.get_total_weight(),box.weight,CONT.max_weight)
                # print(CONT.get_total_occupide_volume(),box.get_volume(),CONT.get_volume())
                # if CONT.get_total_weight() + box.weight > CONT.max_weight or\
                #         CONT.get_total_occupide_volume() + box.volume > CONT.get_volume():
                #     CONT.unfitted_items.append(box)
                #     fit = False

                if CONT.get_total_occupide_volume() + box.get_volume() > CONT.get_volume():
                    CONT.unfitted_items.append(box)
                    fit = False
                if fit:
                    if pos[2] == 0:
                        box.set_onBase(True)
                    box.set_position(pos)
                    box.is_fit = True
                    CONT.fit_items.append(box)
                    # boxes.remove((box, r))
                    if pos[0]+l < L and [pos[0]+l, pos[1], pos[2]] not in PP:
                        temp_pp.append([pos[0]+l, pos[1], pos[2]])
                    if pos[1]+w < W and [pos[0], pos[1]+w, pos[2]] not in PP:
                        temp_pp.append([pos[0], pos[1]+w, pos[2]])
                    if pos[2]+h < H and [pos[0], pos[1], pos[2]+h] not in PP:
                        temp_pp.append([pos[0], pos[1], pos[2]+h])

                    PP.remove(pos)
                    PP.extend(temp_pp)
                    box.set_pps(temp_pp)
                    PP = sorted(PP, key=lambda point: (
                        point[0], point[2], point[1]), reverse=False)
                break
            if box.is_fit == False:
                    CONT.unfitted_items.append(box)
        # print(len(CONT.fit_items), len(CONT.items))
        # print(CONT.get_total_occupide_volume(),CONT.get_volume())
        fitness = [round((CONT.get_total_occupide_volume() / CONT.get_volume() * 100), 2),
                   round((len(CONT.fit_items) / len(CONT.items) * 100), 2),
                   round((CONT.get_total_fitted_item_value() / total_value * 100), 2)]
        ft[key] = fitness
        population[key]['fitness'] = deepcopy(fitness)
        population[key]['result'] = copy.deepcopy(CONT.fit_items)
        population[key]['un_fit_items'] = copy.deepcopy(CONT.unfitted_items)
        CONT.fit_items.clear()
        CONT.unfitted_items.clear()
        # print("...............")
    return population, ft
