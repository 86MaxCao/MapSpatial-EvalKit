import copy
import ast
from PIL import Image, ImageDraw, ImageFont, ImageColor


additional_colors = [colorname for (colorname, colorcode) in ImageColor.colormap.items()]


def plot_bounding_boxes(im, bounding_boxes, input_width, input_height):
    """
    Plots bounding boxes on an image with markers for each a name, using PIL, normalized coordinates, and different colors.

    Args:
        img_path: The path to the image file.
        bounding_boxes: A list of bounding boxes containing the name of the object
         and their positions in normalized [y1 x1 y2 x2] format.
    """
    

    # Load the image
    img = im
    width, height = img.size
    # print(img.size)
    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Define a list of colors
    colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'orange',
    'pink',
    'purple',
    'brown',
    'gray',
    'beige',
    'turquoise',
    'cyan',
    'magenta',
    'lime',
    'navy',
    'maroon',
    'teal',
    'olive',
    'coral',
    'lavender',
    'violet',
    'gold',
    'silver',
    ] + additional_colors

    if bounding_boxes is None:
        # Display the image
        return 
    # font = ImageFont.truetype("NotoSansCJK-Regular.ttc", size=14)
    # Iterate over the bounding boxes
    for i, bounding_box in enumerate(bounding_boxes):
        # Select a color from the list
        if len(bounding_box["bbox_2d"]) != 4:
            continue
        color = colors[i % len(colors)]

        # if bounding_box["bbox_2d"][0] <= 1.:
        #     input_height, input_width = 1., 1.

        # Convert normalized coordinates to absolute coordinates
        abs_x1 = int(bounding_box["bbox_2d"][0]/input_width * width)
        abs_y1 = int(bounding_box["bbox_2d"][1]/input_height * height)
        abs_x2 = int(bounding_box["bbox_2d"][2]/input_width * width)
        abs_y2 = int(bounding_box["bbox_2d"][3]/input_height * height)
        # print(bounding_box["bbox_2d"], abs_x1, abs_y1, abs_x2, abs_y2)

        if abs_x1 > abs_x2:
            abs_x1, abs_x2 = abs_x2, abs_x1

        if abs_y1 > abs_y2:
            abs_y1, abs_y2 = abs_y2, abs_y1
        # print("(abs_x1, abs_y1), (abs_x2, abs_y2):", (abs_x1, abs_y1), (abs_x2, abs_y2), bounding_box["bbox_2d"], input_width, width, input_height, height)
        # print(draw)
        # Draw the bounding box
        draw.rectangle(
            ((abs_x1, abs_y1), (abs_x2, abs_y2)), outline=color, width=4
        )

        # Draw the text
        if "label" in bounding_box:
            draw.text((abs_x1 + 8, abs_y1 + 6), bounding_box["label"], fill=color)    # font=font

    # Display the image


def plot_movement(im, data, input_width, input_height):

    img = im
    width, height = img.size
    draw = ImageDraw.Draw(img)
    colors = ['red', 'blue']  # Assume red for starting, blue for ending
    line_width = 4

    if data is None:
        # Display the image
        return 
    # print("decode json points: ", data, len(data))

    for line in data:
        # Extract starting and ending points
        start_point = line.get("start_point_2d", None)
        end_point = line.get("end_point_2d", None)
        if start_point is None or end_point is None:
            # print("Starting or ending location not found. ", line)
            return

        # if start_point[0] <= 1.:
        #     input_height, input_width = 1., 1.

        # Converting coordinates
        abs_x_start = int(start_point[0]) / input_width * width
        abs_y_start = int(start_point[1]) / input_height * height

        abs_x_end = int(end_point[0]) / input_width * width
        abs_y_end = int(end_point[1]) / input_height * height

        # Draw an arrow from the starting point to the ending point
        draw.line((abs_x_start, abs_y_start, abs_x_end, abs_y_end), fill='black', width=line_width)

        # Draw and annotate start and end points
        for i, point in enumerate([start_point, end_point]):
            color = colors[i % len(colors)]
            abs_x = int(point[0]) / input_width * width
            abs_y = int(point[1]) / input_height * height
            radius = 4
            # label = data[i]["label"]

            draw.ellipse([(abs_x - radius, abs_y - radius), (abs_x + radius, abs_y + radius)], fill=color)
            # draw.text((abs_x + 8, abs_y + 6), label, fill=color)


def safe_eval(item):
    try:
        # Use ast.literal_eval instead of eval for safely evaluating string expressions
        return ast.literal_eval(item)
    except (ValueError, SyntaxError) as e:
        # If parsing fails, log error and return None
        # print(f"Failed to evaluate item: {item}. Error: {e}")
        return None


def parse_json(json_output):
    # Parsing out the markdown fencing
    json_output_list = []
    lines = json_output.splitlines()
    for i, line in enumerate(lines):
        # print(i, line, line.strip()=="```json")
        if line.strip() == "```json":
            tmp = "\n".join(lines[i+1:])  # Remove everything before "```json"
            if "```" in tmp:
                tmp = tmp.split("```")[0]  # Remove everything after the closing "```"
            else:
                tmp = tmp.split("</think>")[0].strip()
            json_output_list.append(tmp)
    return json_output_list


def parse_bbox_and_movement(response):
    parsed_list = parse_json(response)
    parsed_list = [safe_eval(item) for item in parsed_list]
    parsed_list = [item for item in parsed_list if item is not None]      # filter
    bbox_list, movement_list = [], []
    for item_list in parsed_list:
        for item in item_list:
            if "bbox_2d" in item and "label" in item:
                bbox_list.append(item)
            elif "start_point_2d" in item and "end_point_2d" in item and "label" in item:
                movement_list.append(item)
    # for item in bbox_list:
    #     # item = eval(item)
    #     print(type(item), item)
    # print("\n########################")
    # for item in movement_list:
    #     print(type(item), item)
    return bbox_list, movement_list


def merge_bbox_list(bbox_list_origin, bbox_list_new, image_index_new):
    """
    Merge two bounding box lists, ensuring unique bounding boxes per label, prioritizing data from bbox_list_new.
    
    :param bbox_list_origin: Original bounding box list
    :param bbox_list_new: New bounding box list
    :return: Merged bounding box list
    """
    image_index = -1
    if len(bbox_list_new):
        # Build new label dictionary for fast lookup
        new_label_dict = {bbox['label']: bbox for bbox in bbox_list_new}
        merged_bbox_list = []
        
        image_index = [bb['index']-1 for bb in bbox_list_new]
        assert len(set(image_index)) == 1, f"bbox_list_new: {bbox_list_new}"
        image_index = image_index[0]
        if image_index not in bbox_list_origin:
            bbox_list_origin[image_index] = []

        # Iterate over original list, replacing or keeping bounding boxes as needed
        for bbox in bbox_list_origin[image_index]:
            label = bbox['label']
            if label in new_label_dict:
                # Prioritize bounding box from new list, and mark as processed
                merged_bbox_list.append(new_label_dict.pop(label))
            else:
                # Keep bounding box from original list
                merged_bbox_list.append(bbox)

        # Add remaining bounding boxes from new list to result
        merged_bbox_list.extend(new_label_dict.values())
        bbox_list_origin[image_index_new] = copy.deepcopy(merged_bbox_list)
    return image_index, bbox_list_origin


def merge_movement_list(movement_list_origin, movement_list_new, image_index_new):
    """
    Merge two movement direction lists, ensuring unique movement per label, prioritizing data from movement_list_new.
    
    :param movement_list_origin: Original movement direction list
    :param movement_list_new: New movement direction list
    :return: Merged movement direction list
    """
    image_index = -1
    if len(movement_list_new):
        # Build new label dictionary for fast lookup
        new_label_dict = {movement['label']: movement for movement in movement_list_new}
        merged_movement_list = []

        image_index = [mv['index'] - 1 for mv in movement_list_new]
        assert len(set(image_index)) == 1
        image_index = image_index[0]
        if image_index not in movement_list_origin:
            movement_list_origin[image_index] = []

        # Iterate over original list, replacing or keeping movements as needed
        for movement in movement_list_origin[image_index]:
            label = movement['label']
            if label in new_label_dict:
                # Prioritize movement from new list, and mark as processed
                merged_movement_list.append(new_label_dict.pop(label))
            else:
                # Keep movement from original list
                merged_movement_list.append(movement)

        # Add remaining movements from new list to result
        merged_movement_list.extend(new_label_dict.values())
        movement_list_origin[image_index_new] = copy.deepcopy(merged_movement_list)
    return image_index, movement_list_origin


def merge_bbox_movement(bbox_list_origin, movement_list_origin, bbox_list_new, movement_list_new, image_index_new):
    idx1, merged_bbox_list = merge_bbox_list(bbox_list_origin, bbox_list_new, image_index_new)
    idx2, merged_movement_list = merge_movement_list(movement_list_origin, movement_list_new, image_index_new)
    if idx1 >= 0 and idx2 == -1:
        merged_movement_list[image_index_new] = copy.deepcopy(merged_movement_list[idx1])
    # else:
    #     merged_movement_list[image_index_new] = []

    if idx2 >= 0 and idx1 == -1:
        merged_bbox_list[image_index_new] = copy.deepcopy(merged_bbox_list[idx2])
    # else:
    #     merged_bbox_list[image_index_new] = []

    if image_index_new not in merged_bbox_list:
        merged_bbox_list[image_index_new] = []
    if image_index_new not in merged_movement_list:
        merged_movement_list[image_index_new] = []

    return max([idx1, idx2]), merged_bbox_list, merged_movement_list
