from typing import Dict

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import controller as c
import argparse

plt.ion()
fig, ax = plt.subplots()
i = 1

def on_model(rects: Dict[int,c.Rectangle], big_rect: c.Rectangle, maxBoxes: int):
    #define Matplotlib figure and axis
    ax.clear()
    ax.plot()
    #add big rectangle to plot
    ax.add_patch(Rectangle((0, 0), big_rect.width, big_rect.height, edgecolor='black', fill=False, lw=1))
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help="lp-files")
    args = parser.parse_args()
    controller = c.Controller(args.files)
    controller.solve(on_model=on_model)



