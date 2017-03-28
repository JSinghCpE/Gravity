import itertools
import math
import time
import tkinter as tk


class Gravity:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root)
        self.canvas.config(width=900, height=600)
        self.canvas.bind("<Button 1>", self.on_click)
        self.canvas.pack()

        self.particles = []

        self.lastTime = time.time()

        self.root.after(10, self.run)
        self.root.mainloop()

    def run(self):
        self.update()
        self.repaint()
        self.root.after(10, self.run)

    def update(self):
        dt = time.time() - self.lastTime
        new_particles = []
        merged_particles = []

        for pair in itertools.combinations(self.particles, 2):
            relate = self.get_spatial_relationship(pair[0], pair[1])

            if math.sqrt(relate['r2']) < max(pair[0]['r'], pair[1]['r']):
                m = pair[0]['m'] + pair[1]['m']
                r = math.sqrt(m) / 3.14

                x = (pair[0]['x'] * pair[0]['m'] + pair[1]['x'] * pair[1]['m']) / m
                y = (pair[0]['y'] * pair[0]['m'] + pair[1]['y'] * pair[1]['m']) / m

                vx = (pair[0]['vx'] * pair[0]['m'] + pair[1]['vx'] * pair[1]['m']) / m
                vy = (pair[0]['vy'] * pair[0]['m'] + pair[1]['vy'] * pair[1]['m']) / m

                pid = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='#777', outline='')

                new_particles.append({'id': pid, 'm': m, 'r': r,
                                      'x': x, 'y': y,
                                      'vx': vx, 'vy': vy,
                                      'ax': 0, 'ay': 0})

                merged_particles.append(pair[0])
                merged_particles.append(pair[1])

                break

            f_gravity = 400 * pair[0]['m'] * pair[1]['m'] / relate['r2']
            f_x = math.cos(relate['theta']) * f_gravity
            f_y = math.sin(relate['theta']) * f_gravity
            dax0 = f_x / pair[0]['m']
            day0 = f_y / pair[0]['m']
            dax1 = f_x / pair[1]['m']
            day1 = f_y / pair[1]['m']

            pair[0]['ax'] += dax0
            pair[0]['ay'] += day0

            pair[1]['ax'] -= dax1
            pair[1]['ay'] -= day1

        for p in merged_particles:
            self.particles.remove(p)
            self.canvas.delete(p['id'])

        for p in self.particles:
            p['x'] += dt * p['vx']
            p['y'] += dt * p['vy']
            p['vx'] += dt * p['ax']
            p['vy'] += dt * p['ay']
            p['ax'] = 0
            p['ay'] = 0

        for p in new_particles:
            self.particles.append(p)

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

    @staticmethod
    def restrict(x, _min, _max):
        if x < _min:
            return _min
        if x > _max:
            return _max
        return x

    def repaint(self):
        for p in self.particles:
            self.canvas.coords(p['id'], p['x'] - p['r'], p['y'] - p['r'],
                               p['x'] + p['r'], p['y'] + p['r'])

    def on_click(self, event):
        m = 500
        r = math.sqrt(m) / 3.14
        x0 = event.x - r
        y0 = event.y - r
        x1 = event.x + r
        y1 = event.y + r
        pid = self.canvas.create_oval(x0, y0, x1, y1, fill='#777', outline='')
        self.particles.append({'id': pid, 'm': m, 'r': r,
                               'x': event.x, 'y': event.y,
                               'vx': 0, 'vy': 0,
                               'ax': 0, 'ay': 0})


def main():
    game = Gravity()


if __name__ == '__main__':
    main()
