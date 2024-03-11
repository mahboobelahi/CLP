import numpy as np
import matplotlib.pyplot as plt
label = 0
pallete = ['darkgreen', 'tomato', 'yellow', 'darkblue', 'darkviolet', 'indianred', 'yellowgreen', 'mediumblue', 'cyan',
           'black', 'indigo', 'pink', 'lime', 'sienna', 'plum', 'deepskyblue', 'forestgreen', 'fuchsia', 'brown',
           'turquoise', 'aliceblue', 'blueviolet', 'rosybrown', 'powderblue', 'lightblue', 'skyblue', 'lightskyblue',
           'steelblue', 'dodgerblue', 'lightslategray', 'lightslategrey', 'slategray', 'slategrey', 'lightsteelblue',
           'cornflowerblue', 'royalblue', 'ghostwhite', 'lavender', 'midnightblue', 'navy', 'darkblue', 'blue',
           'slateblue', 'darkslateblue', 'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'darkorchid',
           'darkviolet', 'mediumorchid']
color_pallete = ['lightsalmon', 'lightseagreen', 'lavenderblush', 'aquamarine', 'palegreen', 'yellow', 'firebrick', 'maroon', 'darkred', 'red', 'salmon', 'darksalmon', 'coral', 'orangered',
                 'lightcoral', 'chocolate', 'saddlebrown', 'sandybrown', 'olive', 'olivedrab', 'darkolivegreen',
                 'greenyellow', 'chartreuse', 'lawngreen', 'darkseagreen', 'lightgreen', 'limegreen',
                 'green', 'seagreen', 'mediumseagreen', 'springgreen', 'mediumspringgreen', 'mediumaquamarine',
                 'mediumturquoise', 'lightcyan', 'paleturquoise', 'darkslategray',
                 'darkslategrey', 'teal', 'darkcyan', 'aqua', 'cyan', 'darkturquoise', 'cadetblue', 'thistle',
                 'violet', 'purple', 'darkmagenta', 'magenta', 'orchid', 'mediumvioletred', 'deeppink', 'hotpink',
                 'palevioletred', 'crimson', 'lightpink']


def cuboid_data(o, size=(1, 1, 1)):
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1], o[1], o[1]],
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]
    z = [[o[2], o[2], o[2], o[2], o[2]],
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]
    return np.array(x), np.array(y), np.array(z)


def plotcuboid(pos=(0, 0, 0), size=(1, 1, 1), ax=None, lab=label,**kwargs):
    # Plotting a cube element at position pos
    if ax is not None:
        x,y,z =pos
        length ,width, height =size
        X, Y, Z = cuboid_data(pos, size)
        
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                         edgecolor='black', alpha=0.3,linewidth=1.2, edgecolors='r', **kwargs)

        for dx, dy, dz in [(length/2 ,width/2 , height),
                           (length ,width/2 , height/2),(0 ,width/2 , height/2),
                            (length/2 ,0 , height/2),(length/2 ,width , height/2),
                            (length/2 ,width/2 , height*(-.5))]:
            ax.text(x + dx, y + dy, z + dz, str(label),alpha=0, color='black', fontsize=15, ha='center', va='center')

def draw( x_ticks, y_ticks, z_ticks, step_size,pieces, color_index=[], title=""):
    global label
    positions = []
    sizes = []
    colors = []
    sorted_size = []
    decrement =30
    for each in pieces:
        positions.append(each[0:3])
        sizes.append(each[3:])
        sorted_size.append(set(each[3:]))
    if len(color_index) == 0:
        colors = pallete[:len(positions)]
        color_index = [sorted_size, colors]
    else:
        dim = color_index[0]
        clr = color_index[1]
        for each in sorted_size:
            index = dim.index(each)
            colors.append(clr[index])
    plt.interactive(True)
    fig = plt.figure(figsize=(15,20))

    ax = fig.add_subplot(projection='3d')
    ax.set_xticks(np.arange(0, x_ticks + step_size-decriment, step_size-decriment))
    ax.set_yticks(np.arange(0, y_ticks + step_size-40, step_size-40))
    ax.set_zticks(np.arange(0, z_ticks + step_size-40, step_size-40))
    
    for p, s, c in zip(positions, sizes, colors):
        label = label+1
        plotcuboid(pos=p, size=s, ax=ax, color=c,lab=label)
    label =0
    plt.title(title)

    plt.show()

    return color_index

from mpl_toolkits.mplot3d import Axes3D
decriment=30
def plot_3d_rectangle(rectangles, x_ticks, y_ticks, z_ticks, step_size,index):
    plt.interactive(True)
    fig = fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection='3d')
    s=['SS',"TS","BS","FS"]
    label =1
    for rect in rectangles:
        x, y, z, length, width, height,i,partno = rect
        # if i== 0:
        #     #ax.bar3d(x, y, z, length, width, height, color='none', edgecolor='black', lw=4)
        #     ax.bar3d(x, y, z, length, width, height,color='none',alpha=0.1, edgecolor=(0, 0, 0, 1), lw=5)

        # else:
        ax.bar3d(x, y, z, length, width, height,color=pallete[i],alpha=.2, edgecolor=(0, 0, 0, 1), lw=3)
                # Generate and plot vertices
        # vertices = [
        #     (x + length, y, z),  # (xi+li, yi, zi)
        #     (x, y + width, z),  # (xi, yi+wi, zi)
        #     (x, y, z + height)   # (xi, yi, zi+hi)
        # ]
        # for vertex in vertices:
        #     ax.scatter(*vertex, color='black', s=50)
 # Add label to the top face
        for dx, dy, dz in [#(length/2 ,width/2 , height),#top face
                            (length/2 ,width/2 , height/2)
                            #(0 ,width/2 , height/2),
                            #(length/2 ,0 , height/2),#right to top face
                            #(length/2 ,width , height/2),#left to top face
                            #(length/2 ,width/2 , height*(-.5))
                                ]:
                ax.text(x + dx, y + dy, z + dz, partno, color='black', fontsize=15, ha='center', va='center')

        label =label+1
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('3D Rectangles')

    ax.set_xticks(np.arange(0, x_ticks + step_size-decriment, step_size-decriment))
    ax.set_yticks(np.arange(0, y_ticks + step_size-40, step_size-40))
    ax.set_zticks(np.arange(0, z_ticks + step_size-40, step_size-40))
    #plt.savefig(f"Figure{label}.png", format="png", dpi=1200)
    plt.show()

