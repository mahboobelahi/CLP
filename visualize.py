import numpy as np
import matplotlib.pyplot as plt

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

