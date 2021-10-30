from typing import Dict

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import controller as c

plt.ion()
fig, ax = plt.subplots()
i = 1

def on_model(rects: Dict[int,c.Rectangle], maxBoxes: int):
    #define Matplotlib figure and axis
    ax.clear()
    ax.plot()
    #add big rectangle to plot
    ax.add_patch(Rectangle((0, 0), big_rect_width, big_rect_height, edgecolor='black', fill=False, lw=1))
    ax.set_aspect('equal', 'box')
    numRotated = 0
    #add rectangle to plot
    for key, rect in rects.items():
        obj_rect = Rectangle((rect.x_pos, rect.y_pos), rect.width, rect.height, edgecolor='blue', fill=False, lw=1)
        ax.add_patch(obj_rect)
        rx, ry = obj_rect.get_xy()
        cx = rx + obj_rect.get_width()/2.0
        cy = ry + obj_rect.get_height()/2.0
        
        if rect.isRotated:
            numRotated +=1
        ax.annotate(str(key) + ('r' if rect.isRotated else ''), (cx, cy), color='b', weight='bold', 
                    fontsize=6, ha='center', va='center')
    global i
    ax.set_title(f'Model: {i}, Rects: {len(rects)}/{numRotated} ({maxBoxes})')
    i+=1
    fig.canvas.draw()
    fig.canvas.flush_events()

big_rect_height = 1500
big_rect_width = 1300
rect_dim_width = 223
rect_dim_height = 247

controller = c.Controller()
controller.solve(c.Dimension(big_rect_width, big_rect_height),
                 c.Dimension(rect_dim_width, rect_dim_height),
                 on_model=on_model)





