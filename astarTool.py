import tkinter as tk
from queue import PriorityQueue
import threading
import time

RED = "red"
GREEN = "green"
BLUE = "blue"
YELLOW = "yellow"
WHITE = "white"
BLACK = "black"
PURPLE = "purple"
ORANGE = "orange"
GREY = "gray"
TURQUOISE = "turquoise"
WIDTH = 600
HEIGHT = 510
ROW = 20
COL = 17
S = None
E = None
LIST = [False,False,False,False]
Grid_map = [[1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1]]


class Spot:
    def __init__(self, row, col, width, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = row * width+15
        self.y = col * width+13
        self.pos = (self.row,self.col)
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.d = None

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        if not(self.is_start()) and not(self.is_end()) and not(self.is_barrier()):
            self.color = RED

    def make_open(self):
        if not(self.is_start()) and not(self.is_end()) and not(self.is_barrier()):
            self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self,path):
        if not(self.is_start()) and not(self.is_end()):
            self.color = PURPLE
        dot = [self.row,self.col]
        # print(dot)
        path.append(dot)
        # print(path)
        return path

    def draw(self, canvas):
        if self.color != WHITE and self.color != BLACK and self.color != RED and self.color != GREEN:
            self.d = canvas.create_rectangle(self.x, self.y, self.width+self.x-2, self.width+self.y-2,fill=self.color, width=2)

    def delete(self, canvas):
        if self.d != None:
            canvas.delete(self.d)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

class Brain:
    def __init__(self,S,E,path):
        self.S = S
        self.E = E
        self.path = path
        self.path2 = []
        self.path_if_dot = [False,False,False,False]
        self.path_dot_dir = []
        self.path_pos = []
        self.Start = False

    def h(self,p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self,came_from, current, draw):
        while current in came_from:
            current = came_from[current]
            self.path = current.make_path(self.path)
            # draw()

    def algorithm(self,draw, grid, start, end):
        self.path = []
        self.path2 = []
        self.Start = True
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())

        open_set_hash = {start}
        count = 0
        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                draw()
                self.reconstruct_path(came_from, end, draw)
                draw()
                end.make_end()
                self.path.reverse()
                self.path2 = self.colculate_path(self.path)
                self.adjust_path(self.path)
                print(self.path_if_dot)
                print(self.path_dot_dir)
                print(self.path_pos)
                self.Start = False
                return self.path

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
            if count%5==0:
                draw()
            count+=1
            if current != start:
                current.make_closed()
        return None

    def colculate_path(self,path):
        # new_path = [False,False,False,False]
        print("test")
        new_path = []
        for i in range(len(path)-1):
            if path[i][0]!=path[i+1][0]:
                if path[i][0]>path[i+1][0]:#left
                    new_path.append("left")
                else :#right
                    new_path.append("right")
            elif path[i][1]!=path[i+1][1]:
                if path[i][1]>path[i+1][1]:#up
                    new_path.append("up")
                else :#down
                    new_path.append("down")
        return new_path

    def adjust_path(self, path):
        self.path_if_dot = [False,False,False,False]
        self.path_dot_dir = []
        self.path_pos = []
        for i in range(len(path)-1):
            if path[i]==[6,4] or path[i]==[5,4] or path[i]==[6,5] or path[i]==[5,5]:
                if self.path_if_dot[0] == False:
                    self.path_if_dot[0] = True
                    self.path_dot_dir.append(self.path2[i])
                    self.path_pos.append(self.path[i])
                else:
                    n = len(self.path_dot_dir)
                    self.path_dot_dir[n-1] = self.path2[i]
                    self.path_pos[n-1] = self.path[i]

            elif path[i]==[6,10] or path[i]==[5,10] or path[i]==[6,11] or path[i]==[5,11]:
                if self.path_if_dot[1] == False:
                    self.path_if_dot[1] = True
                    self.path_dot_dir.append(self.path2[i])
                    self.path_pos.append(self.path[i])
                else:
                    n = len(self.path_dot_dir)
                    self.path_dot_dir[n-1] = self.path2[i]
                    self.path_pos[n-1] = self.path[i]
            elif path[i]==[13,4] or path[i]==[12,4] or path[i]==[13,5] or path[i]==[12,5]:
                if self.path_if_dot[2] == False:
                    self.path_if_dot[2] = True
                    self.path_dot_dir.append(self.path2[i])
                    self.path_pos.append(self.path[i])
                else:
                    n = len(self.path_dot_dir)
                    self.path_dot_dir[n-1] = self.path2[i]
                    self.path_pos[n-1] = self.path[i]
            elif path[i]==[13,10] or path[i]==[12,10] or path[i]==[13,11] or path[i]==[12,11]:
                if self.path_if_dot[3] == False:
                    self.path_if_dot[3] = True
                    self.path_dot_dir.append(self.path2[i])
                    self.path_pos.append(self.path[i])
                else:
                    n = len(self.path_dot_dir)
                    self.path_dot_dir[n-1] = self.path2[i]
                    self.path_pos[n-1] = self.path[i]
            elif i == 0:
                self.path_dot_dir.append(self.path2[i])
                self.path_pos.append(self.path[i])

        self.path_dot_dir.append(self.path2[len(self.path2)-1])
        self.path_pos.append(self.path[len(self.path)-1])
        return


def make_grid(rows, cols, width):
        grid = []
        gap = width // rows#30
        for i in range(rows):
            grid.append([])
            for j in range(cols):
                spot = Spot(i, j, gap, rows, cols)
                if Grid_map[j][i] == 1:
                    spot.make_barrier()
                elif Grid_map[j][i] == 2:
                    spot.make_start()
                elif Grid_map[j][i] == 3:
                    spot.make_end()
                grid[i].append(spot)
        return grid

def draw(canvas, grid, width):
        for row in grid:
            for spot in row:
                spot.draw(canvas)



