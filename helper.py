import copy


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


def get_vertices(box):
    # Extract dimensions of the rectangle
    x, y, z, l, w, h = box
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
    # a = value["un_fit_items"]
    # b = {"quantity": len(value["un_fit_items"]),
    #      "item_ids": [i.get_id() for i in value["un_fit_items"]]}
    # result["cargo_metadata"]["packed_items"] = len(res)
    # result["cargo_metadata"]["unpacked_items"]["quantity"] = len(
    #     value["un_fit_items"])
    # result["cargo_metadata"]["unpacked_items"]["item_ids"] = [i.get_id()
    #                                                           for i in value["un_fit_items"]]

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
                "left": [neighbor.get_id() for neighbor in item.besideL if neighbor],
                "right": [neighbor.get_id() for neighbor in item.besideR if neighbor],
                "top": [[neighbor[0].get_id(), neighbor[1]] for neighbor in item.top if neighbor],
                "under": [[neighbor[0].get_id(), neighbor[1]] for neighbor in item.under if neighbor],
                "back": [neighbor.get_id() for neighbor in item.back if neighbor],
                "front": [neighbor.get_id() for neighbor in item.front if neighbor],
            }
        } for item in res]
    result[f"{p_ind}{key}"] = {
                               "solution_fitness": value["fitness"],
                               "packed_items": len(res),
                               "unpacked_items": {
                                   "quantity": len(value["un_fit_items"]),
                                   "item_ids": [i.get_id() for i in value["un_fit_items"]]
                               }, "num": len(value['result']),
                               "item_passport": itesm_passport,}
    return result


def remove_pp(area, CONT, removed_PP, pos):
    if area < .30:
        removed_PP.append(pos)
        CONT.PP.remove(pos)
