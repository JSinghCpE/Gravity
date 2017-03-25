import math
import time
import tkinter as tk


class Gravity:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root)
        self.canvas.bind("<Button 1>", self.on_click)
        self.canvas.pack()

        self.points = []

        self.lastTime = time.time()

        self.root.after(10, self.run)
        self.root.mainloop()

    def run(self):
        self.update()
        self.repaint()
        self.root.after(10, self.run)

    def update(self):
        dt = time.time() - self.lastTime
        for p1 in self.points:
            p1['ax'] = 0
            p1['ay'] = 0
            for p2 in self.points:
                if p1 == p2:
                    continue

                relate = self.get_spatial_relationship(p1, p2)
                f_gravity = 100 * p1['m'] * p2['m'] / relate['r2']
                f_x = math.sin(relate['theta']) * f_gravity
                f_y = math.cos(relate['theta']) * f_gravity
                dax = f_x / p1['m']
                day = f_y / p1['y']

                print("dx: ", relate['dx'], ", dy: ", relate['dy'], ", theta: ", relate['theta'])

                # if relate['dx'] < 0:
                #     p1['ax'] -= dax
                # else:
                #     p1['ax'] += dax
                # if relate['dy'] < 0:
                #     p1['ay'] += day
                # else:
                #     p1['ay'] -= day

            p1['vx'] += p1['ax'] * dt
            p1['vy'] += p1['ay'] * dt
            p1['x'] += p1['vx'] * dt
            p1['y'] += p1['vy'] * dt
        self.lastTime += dt

    @staticmethod
    def get_spatial_relationship(p1, p2):
        dx = p2['x'] - p1['x']
        dy = p2['y'] - p1['y']
        r2 = math.pow(dx, 2) + math.pow(dy, 2)
        theta = math.atan2(dy, dx)
        while theta < 0.0:
            theta += 2 * math.pi
        return {'dx': dx, 'dy': dy,
                'r2': r2, 'theta': theta}

    def repaint(self):
        for p in self.points:
            self.canvas.coords(p['id'], p['x'] - 2, p['y'] - 2, p['x'] + 2, p['y'] + 2)

    def on_click(self, event):
        self.points.append({'id': self.canvas.create_rectangle(event.x - 2, event.y - 2, event.x + 2, event.y + 2),
                            'x': event.x, 'y': event.y,
                            'vx': 0, 'vy': 0,
                            'ax': 0, 'ay': 0, 'm': 100})


def main():
    game = Gravity()


if __name__ == '__main__':
    main()
