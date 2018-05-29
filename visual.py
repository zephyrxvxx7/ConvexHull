import tkinter as tk
from random import randint




class MainApplication:
    canvas_width = 500
    canvas_height = 500

    ROUND = 100

    points = list()

    def __init__(self, master):

        tk.Label(master, text="點的數量").grid(row=0)

        self.inp = tk.Entry(master,
                       textvariable = tk.StringVar(),
                       validate = 'key',
                       validatecommand=(master.register(self.digit_test), '%P')
                       )
        self.inp.insert(10, "100")
        self.inp.grid(row=0, column=1)

        tk.Button(master, text='產生', command=self.produce_points).grid(row=0, column=2)

        tk.Label(master, text="Press and Drag the mouse to draw").grid(row = 1, columnspan = 3)

        self.canvas = tk.Canvas(master,
                        width = self.canvas_width,
                        height = self.canvas_height)
        self.canvas.grid(row=2, columnspan=3)
        self.canvas.bind("<B1-Motion>", self.paint)

        tk.Button(master, text='開始Convex Hull',
                  command=self.paint_convex_hull).grid(row=3, columnspan=3)

        

    def paint(self, event):
        self.canvas.create_oval(event.x, event.y, event.x, event.y, fill = "black", tags = "points")
        self.points.append([event.x, event.y])
    
    def paint_line(self, *args, **xargs):
        self.canvas.create_line(*args, **xargs)

    def paint_point(self, x, y):
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black", tags="points")

    def paint_points(self, point):
        for (x, y) in point:
            self.paint_point(x, y)

    def clr(self):
        self.canvas.delete("all")
    
    def del_lines(self):
        self.canvas.delete("lines")
    
    def del_points(self):
        self.canvas.delete("points")

    def produce_points(self):
        self.clr()

        if self.inp.get() != '':
            self.ROUND = int(self.inp.get())

        self.points = [[randint(3, 497), randint(3, 497)] for _ in range(self.ROUND)]

        self.paint_points(self.points)
    
    def digit_test(self, content):
        if content.isdigit() or (content == ""):
            return True
        else:
            return False
    
    #--- convex hull ---
    def cross(self, A, B, C):
        return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])
    
    def length2(self, A, B):
        return (A[0] - B[0]) * (A[0] - B[0]) + (A[1] - B[1]) * (A[1] - B[1])
    
    def far(self, O, A, B):
        if self.length2(O, A) > self.length2(O, B):
            return True
        else:
            return False

    def jarvismarch(self):
        minPoint = self.points[0]
        start = 0
        CH = list()
        
        for i in range(1, len(self.points)):
            if self.points[i][1] < minPoint[1] or (self.points[i][1] == minPoint[1] and self.points[i][0] < minPoint[0]):
                minPoint = self.points[i]
                start = i
        
        CH.append(minPoint)
        

        while True:
            nextStep = start
            for i in range(1, len(self.points)):
                cross = self.cross(CH[-1], self.points[i], self.points[nextStep])
                if cross > 0 or (cross == 0 and self.far(CH[-1], self.points[i], self.points[nextStep])):
                    nextStep = i
            if nextStep == start:
                break
            CH.append(self.points[nextStep])
        return CH

    def paint_convex_hull(self):
        try:
            lines = self.jarvismarch()
            print(lines)
            for i in range(len(lines)):
                self.canvas.create_oval([lines[i][0], lines[i][1]], [lines[i][0], lines[i][1]], outline="red", fill="yellow")

            self.canvas.create_line(lines[0:len(lines)], fill='blue')
            self.canvas.create_line(
                lines[len(lines) - 1], lines[0], fill='blue')
        except:
            self.clr()