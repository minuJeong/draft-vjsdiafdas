
"""
abstract drawing balls

author: minu jeong
"""

import random
import math
from PIL import Image


class Stage(object):
    w = 1024
    h = 1024
    renderables = []
    render_buffer = None

    def __init__(self):
        self.render_buffer = Image.new("RGBA", (self.w, self.h))

    @property
    def size(self):
        return (self.w, self.h)

    def is_outside(self, x, y):
        return x >= self.w or y >= self.h or x < 0 or y < 0

    def add_child(self, renderable):
        if renderable is None:
            return

        self.renderables.append(renderable)

    def remove_child(self, renderable):
        if renderable in self.renderables:
            self.renderables.remove(renderable)

    def render(self):
        pixels = self.render_buffer.load()

        m = len(self.renderables)
        for i, ball in enumerate(self.renderables):
            print(f"{i} / {m}", end="\r")
            for px, py, v in ball.render():
                v2 = min(pixels[px, py][3] + int(v), 255)
                pixels[px, py] = (v2, v2, v2, v2)

    def save(self, path):
        self.render_buffer.save(path)


class Renderable(object):
    def render(self):
        raise NotImplementedError()


class Coorded(Renderable):
    x = 0
    y = 0


class Ball(Coorded):
    stage = None
    intensity = 1.0
    radius = 24.0
    render_radius = 96.0

    def __init__(self, stage):
        self.stage = stage
        stage.add_child(self)

    def rand_intensity(self, mini, maxi):
        self.intensity = random.random() * (maxi - mini) + mini
        return self

    def rand_rad(self, minr, maxr):
        self.radius = random.random() * (maxr - minr) + minr
        self.render_radius = self.radius * 4.0
        return self

    def rand_pos(self, size):
        self.x = random.randrange(0, size[0])
        self.y = random.randrange(0, size[1])
        return self

    def render(self):
        render_area = []

        x = self.x
        minx = math.floor(x - self.render_radius)
        maxx = math.ceil(x + self.render_radius)

        y = self.y
        miny = math.floor(y - self.render_radius)
        maxy = math.ceil(y + self.render_radius)

        for px in range(minx, maxx):
            for py in range(miny, maxy):
                d = math.sqrt(math.pow(px - x, 2) + math.pow(py - y, 2))
                if self.stage.is_outside(px, py):
                   continue

                v = self.intensity if d == 0 else min(self.radius / (d * 4.0), self.intensity)
                v = math.pow(v, 2.5) * 255
                render_area.append((px, py, v))
        return render_area

def rand_balls(stage, count):
    for ball in [Ball(stage) for _ in range(count)]:
        ball.rand_pos(stage.size)\
            .rand_rad(5.0, 25.0)\
            .rand_intensity(0.1, 1.0)

def main():
    stage = Stage()
    rand_balls(stage, 1024)
    stage.render()
    stage.save("res.png")


if __name__ == "__main__":
    main()
