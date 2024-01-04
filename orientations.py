import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Define the dimensions of the container
container_length = 8
container_width = 8
container_height = 8

# Function to generate a random box with random dimensions and orientations
def generate_random_box():
    length = np.random.uniform(1, 4)  # Random box length between 1 and 4
    width = np.random.uniform(1, 4)   # Random box width between 1 and 4
    height = np.random.uniform(1, 4)  # Random box height between 1 and 4
    orientation = np.random.choice(range(1, 7))  # Random orientation from 1 to 6
    return length, width, height, orientation

# Function to calculate the box position based on its orientation
def calculate_box_position(box, orientation):
    if orientation == 1:
        return box
    elif orientation == 2:
        return [box[1], box[0], box[2]]
    elif orientation == 3:
        return [box[2], box[1], box[0]]
    elif orientation == 4:
        return [box[1], box[0], box[2]]
    elif orientation == 5:
        return [box[2], box[0], box[1]]
    elif orientation == 6:
        return [box[0], box[2], box[1]]

# Create a 3D plot for visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize a list to store the boxes and their positions
boxes = []

# Generate and place random boxes inside the container
while True:
    length, width, height, orientation = generate_random_box()
    position = calculate_box_position([length, width, height], orientation)
    if np.all(np.array(position) <= [container_length, container_width, container_height]):
        boxes.append((position, length, width, height))
    if len(boxes) >= 10:  # Generate and place 10 boxes as an example
        break

# Visualize the container and boxes
for box in boxes:
    position, length, width, height = box
    vertices = [
        [position[0], position[1], position[2]],
        [position[0] + length, position[1], position[2]],
        [position[0] + length, position[1] + width, position[2]],
        [position[0], position[1] + width, position[2]],
        [position[0], position[1], position[2] + height],
        [position[0] + length, position[1], position[2] + height],
        [position[0] + length, position[1] + width, position[2] + height],
        [position[0], position[1] + width, position[2] + height]
    ]
    vertices = np.array(vertices)

    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[0], vertices[3], vertices[7], vertices[4]]
    ]

    ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.5))

ax.set_xlim([0, container_length])
ax.set_ylim([0, container_width])
ax.set_zlim([0, container_height])

plt.show()

