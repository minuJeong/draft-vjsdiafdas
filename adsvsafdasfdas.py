
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
        self.render_buffer = Image.new("RGBA", (self.w, self.h), "BLACK")

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
                if self.is_outside(px, py):
                    continue

                v2 = min(pixels[px, py][0] + int(v * 255), 255)
                pixels[px, py] = (v2, v2, v2, 255)

        return self

    def save(self, path):
        self.render_buffer.save(path)


class Renderable(object):
    stage = None
    intensity = 1.0

    def __init__(self, stage):
        self.stage = stage
        stage.add_child(self)

    def rand_intensity(self, mini, maxi):
        self.intensity = random.random() * (maxi - mini) + mini
        return self

    def render(self):
        raise NotImplementedError()


class Coorded(Renderable):
    x = 0
    y = 0

    def rand_pos(self):
        self.x = random.randrange(0, self.stage.w)
        self.y = random.randrange(0, self.stage.h)
        return self


class Ball(Coorded):
    glow = 2.0
    radius = 24.0
    render_radius = 96.0

    def rand_rad(self, minr, maxr):
        self.radius = random.random() * (maxr - minr) + minr
        self.render_radius = self.radius * 2.0
        return self

    def rand_glow(self, ming, maxg):
        self.glow = random.random() * (maxg - ming) + ming
        return self

    def render(self):
        render_area = []

        x = self.x
        minx = math.floor(x - self.render_radius)
        maxx = math.ceil(x + self.render_radius)

        y = self.y
        miny = math.floor(y - self.render_radius)
        maxy = math.ceil(y + self.render_radius)

        i = self.intensity
        r = self.radius

        for px in range(minx, maxx):
            for py in range(miny, maxy):
                dx = px - x
                dy = py - y
                d = dx * dx + dy * dy
                v = min(r / (d * 2.0 + 0.01), i)
                v *= v
                render_area.append((px, py, v))
        return render_area

class Rect(Coorded):
    w = 1
    h = 1

    @property
    def render_rect(self) -> tuple:
        return (self.x, self.y, self.w, self.h)

    def rand_size(self, mins, maxs):
        self.w = random.random() * (maxs - mins) + mins
        self.h = self.w
        return self

    def render(self):
        render_area = []

        minx = math.floor(self.x)
        maxx = math.ceil(self.x + self.w)

        miny = math.floor(self.y)
        maxy = math.ceil(self.y + self.h)

        for px in range(minx, maxx):
            for py in range(miny, maxy):
                render_area.append((px, py, self.intensity))

        return render_area

def rand_balls(stage, count) -> None:
    for ball in [Ball(stage) for _ in range(count)]:
        ball.rand_pos()\
            .rand_rad(3.0, 22.0)\
            .rand_intensity(0.1, 1.0)\
            .rand_glow(2.0, 3.5)

def rand_rects(stage, count) -> None:
    for rect in [Rect(stage) for _ in range(count)]:
        rect.rand_pos()\
            .rand_size(0.5, 20)\
            .rand_intensity(0.1, 1.0)\

def main():
    stage = Stage()
    rand_balls(stage, 1024)
    rand_rects(stage, 512)
    stage.render()\
         .save("res.png")


if __name__ == "__main__":
    main()
