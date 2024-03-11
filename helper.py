
def check_hanging(box1, box2):
    # Check if the bottom face of the box is either on the container floor or resting on another box
    x, y, z, l, w, h = box1

    # # Check if the bottom face of the box is on the container floor
    if box2[2] == 0:
        return False  # Box is not hanging

    # # Check if the bottom face of the box is resting on another box

    if (box1[0:2] == box2[0:2] and box1[2] + box1[5] == box2[2]):
        return False  # Box is not hanging
    else:
        return True
    # return True  # Box is hanging in the air
    # print(x < box2[0] + box2[3])
    # print(x + l > box2[0])
    # print(y < box2[1] + box2[4])
    # print(y + w > box2[1])
    # print(z == box2[2] + box2[5])

    # if (x < box2[0] + box2[3] and
    # x + l > box2[0] and
    # y < box2[1] + box2[4] and
    # y + w > box2[1] and
    # z == box2[2] + box2[5]):
    #     return False  # Box is not hanging
    # return True  # Box is hanging in the air


def rectIntersect(box1, box2, x, y):
    position, d1 = (box1[0:3], box1[3:6])
    position2, d2 = (box2[0:3], box2[3:6])

    cx1 = position[x] + d1[x]/2
    cy1 = position[y] + d1[y]/2
    cx2 = position2[x] + d2[x]/2
    cy2 = position2[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(box1, box2):
    return (
        rectIntersect(box1, box2, 0, 1) and
        rectIntersect(box1, box2, 1, 2) and
        rectIntersect(box1, box2, 0, 2)
    )


def calculate_overlap_area(rect1, rect2):
    x1, y1, z1, l1, w1, h1 = rect1
    x2, y2, z2, l2, w2, h2 = rect2

    # Calculate the coordinates of the intersection rectangle
    x_overlap = max(0, min(x1+l1, x2+l2) - max(x1, x2))
    y_overlap = max(0, min(y1+w1, y2+w2) - max(y1, y2))

    # Calculate the area of overlap
    overlap_area = x_overlap * y_overlap

    # Calculate the total area of the upper rectangle
    upper_area = l2 * w2

    # Calculate the support percentage
    support_percentage = overlap_area / upper_area

    return round(support_percentage, 2)


# def calculate_overlap_area(rect1, rect2):
#     x1, y1, z1, l1, w1, h1 = rect1
#     x2, y2, z2, l2, w2, h2 = rect2

#     # Calculate the coordinates of the intersection rectangle
#     x_overlap = max(0, min(x1+l1, x2+l2) - max(x1, x2))
#     y_overlap = max(0, min(y1+w1, y2+w2) - max(y1, y2))

#     # Create sets of X and Y coordinates for the two rectangles
#     x_set1 = set(range(x1, x1+l1))
#     y_set1 = set(range(y1, y1+w1))
#     x_set2 = set(range(x2, x2+l2))
#     y_set2 = set(range(y2, y2+w2))

#     # Calculate the area of overlap using sets
#     overlap_area = len(x_set1 & x_set2) * len(y_set1 & y_set2)

#     # Calculate the total area of the smaller rectangle
#     total_area = min(l1 * w1, l2 * w2)

#     # Calculate the percentage of overlap
#     overlap_percentage = overlap_area / total_area

#     return round(overlap_percentage,2)


def get_vertices(box):
    # Extract dimensions of the rectangle
    x, y, z, l, w, h = box

    # Calculate the coordinates of all vertices of the rectangle
    # print({
    #     "FBL":[x, y, z],  # Front bottom left
    #     "FBR": [x + l, y, z],  # Front bottom right
    #     "FTL":[x, y , z+h],  # Front top left
    #     "FTR":[x + l, y , z+h],  # Front top right
    #     "BBL":[x, y+w, z],  # Back bottom left
    #     "BBR":[x + l, y+w, z],  # Back bottom right
    #     "BTL":[x, y + w, z + h],  # Back top left
    #     "BTR":[x + l, y + w, z + h]  # Back top right
    # })
    return {
        "FBL": [x, y, z],  # Front bottom left
        "FBR": [x + l, y, z],  # Front bottom right
        "FTL": [x, y, z+h],  # Front top left
        "FTR": [x + l, y, z+h],  # Front top right
        "BBL": [x, y+w, z],  # Back bottom left
        "BBR": [x + l, y+w, z],  # Back bottom right
        "BTL": [x, y + w, z + h],  # Back top left
        "BTR": [x + l, y + w, z + h]  # Back top right
    }


def get_projections(box1, box2):
    projections = []
    if (box2[0]+box2[3] > box1[0]+box1[3]) and box1[5] == box2[2]:
        vertices = get_vertices(box2)
        vertices["FBR"][2] = 0
        # vertices["BBR"][2]=0
        projections.append(vertices["FBR"])
        # projections.append(vertices["BBR"])
    if (box1[1]+box1[4] < box2[1]+box2[4]) and box1[5] == box2[2]:
        vertices = get_vertices(box2)
        vertices["BBL"][2] = 0
        # vertices["BBR"][2]=0
        projections.append(vertices["BBL"])
    return projections


def clear_neighbors(item, box):

    if box.under:
        # * under: [[box_obj,area]]
        for b in box.under[0][0].top:
            if box in b:
                box.under[0][0].top.remove(b)
        # box_under = box.under[0]
        # box_top = None
        # if box.under[0][0].top:
        #     box_top = box.under[0][0].top[0]
        #     # print(box_under)
        #     if box_top in box_under[0].top:
        #         box_under[0].top.remove(box_top)
        # if box_top:
        #     if box_under in box_top[0].under:
        #         box_top[0].under.remove(box_under)
    if box.besideL:
        if box in box.besideL[0].besideR:
            box.besideL[0].besideR.remove(box)

    if box.besideR:
        if box in box.besideR[0].besideL:
            box.besideR[0].besideL.remove(box)
    if box.back:
        box_back = box.back[0]
        box_front = box_back.front[0]

        if box_back in box_front.back:
            box_front.back.remove(box_back)
        if box_front in box_back.front:
            box_back.front.remove(box_front)
    box.besideR.clear()
    box.besideL.clear()
    box.under.clear()
    box.top.clear()
    box.front.clear()
    box.back.clear()


def get_top_boxes(boxes):
    """
    Recursively get all top boxes starting from the given list of boxes.
    """
    top_boxes = []

    for b in boxes:
        # print(f"Checking box {b[0].get_id()} with top boxes {b[0].top}")

        top_boxes.append(b[0])
        top_boxes.extend(get_top_boxes(b[0].top))
    # print(f"Returning top boxes {top_boxes}")
    return top_boxes


def generate_report(result, value, p_ind, key):
    res = value['result']
    itesm_passport = [
        {
            "id": item.get_id(),
            "customer_belonging": item.name,
            "volume": item.get_volume(),
            "weight": item.weight,
            "material": "",
            "rotation_type": item.rotation_type,
            "dimention_before_rotation": item.get_LWH_R()[0:3],
            "dimention_after_rotation": item.get_dimention()[0:3],
            "plot_data": item.get_plot_data(),
            "on_base": item.onBase, "stackable": "",
            "neighboring_items": {
                # .besideL],
                "left": [neighbor.get_id() for neighbor in item.besideL if neighbor],
                # .besideR],
                "right": [neighbor.get_id() for neighbor in item.besideR if neighbor],
                "top": [[neighbor[0].get_id(), neighbor[1]] for neighbor in item.top if neighbor],
                "under": [[neighbor[0].get_id(), neighbor[1]] for neighbor in item.under if neighbor],
                # .back],
                "back": [neighbor.get_id() for neighbor in item.back if neighbor],
                # .front]
                "front": [neighbor.get_id() for neighbor in item.front if neighbor],
            }
        } for item in res]
    result[f"{p_ind}{key}"] = {"item_passport": itesm_passport,
                               "solution_fitness": value["fitness"],
                               "num": len(value['result'])}
    return result


def remove_pp(area, CONT, removed_PP, pos):
    if area < .30:
        removed_PP.append(pos)
        CONT.PP.remove(pos)

#! ////////////////////////////////////////////
# def is_projection_needed(item,box):
# def is_bottom_touching_top(box1, box2):
#     # Extract coordinates of the bottom face of box2
#     bottom_face_box2_z = box2[2]
#     bottom_face_box2_x_max = box2[0] + box2[3]
#     bottom_face_box2_y_max = box2[1] + box2[4]

#     # Extract coordinates of the top face of box1
#     top_face_box1_z = box1[2] + box1[5]
#     top_face_box1_x_max = box1[0] + box1[3]
#     top_face_box1_y_max = box1[1] + box1[4]

#     # Check if the bottom face of box2 is touching the top face of box1
#     if (bottom_face_box2_z == top_face_box1_z and
#         bottom_face_box2_x_max == top_face_box1_x_max and
#         bottom_face_box2_y_max == top_face_box1_y_max):
#         return True
#     else:
#         return False

# def calculate_corners(rectangle):
#     x, y, z, l, w, h = rectangle

#     # Calculate coordinates of bottom left corner
#     bottom_left_corner = [x, y, z]

#     # Calculate coordinates of top right corner
#     top_right_corner = [x + l, y + w, z + h]

#     return (bottom_left_corner[0:2]+ top_right_corner[0:2])

# def check_overlap(box1, box2):
#     # Check if any corner of box1 lies within the volume occupied by box2
#     R1 =  calculate_corners(box1)
#     R2 =  calculate_corners(box2)


#     widthIsPositive = min(R1[2],R2[2]) > max(R1[0],R2[0])
#     lengthIsPositive = min(R1[3],R2[3]) > max(R1[1],R2[1])
#     if (widthIsPositive and lengthIsPositive) :
#         return check_hanging(box1, box2)

#     else: return (widthIsPositive and lengthIsPositive)
