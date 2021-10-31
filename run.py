import argparse
import enum
import multiprocessing as mp
from queue import Empty
from typing import Dict

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import controller as c


class SIGNALS(str, enum.Enum):
    finished = "FINISHED"


def drawing(queue: mp.Queue):
    try:
        plt.ion()
        fig, ax = plt.subplots()
        i = 1
        while True:
            try:
                msg =  queue.get(timeout=0.1)
                if msg == SIGNALS.finished:
                    plt.ioff()
                    plt.show()
                    return
                (rects, big_rect, maxBoxes) = msg
                #define Matplotlib figure and axis
                ax.clear()
                ax.plot()
                #add big rectangle to plot
                ax.add_patch(Rectangle((0, 0), big_rect.width, big_rect.height, edgecolor='black', fill=False, lw=1))
                ax.set_aspect('equal', 'box')
                numRotated = 0
                #add rectangles to plot
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
                ax.set_title(f'Model: {i}, Rects: {len(rects)}/{numRotated} ({maxBoxes})')
                i+=1
                fig.canvas.draw()
            except Empty:
                pass
            finally:
                fig.canvas.flush_events()
    except KeyboardInterrupt:
        print("Interrupted")
    except Exception:
        # happens when closing figure manually
        # not very clean solution, but it works
        print("Figure closed manually")
        pass
        

def run(files, queue: mp.Queue):
    controller = c.Controller(files)

    def _on_model(rects: Dict[int,c.Rectangle], big_rect: c.Rectangle, maxBoxes: int):
        queue.put((rects, big_rect, maxBoxes))

    controller.solve(on_model=_on_model)
    queue.put(SIGNALS.finished)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help="lp-files")
    args = parser.parse_args()
    queue = mp.Queue()
    p = mp.Process(target=run, args=(args.files,queue))
    p.start() # start solver
    drawing(queue)
    p.kill() # kill solver-process if still running
    



