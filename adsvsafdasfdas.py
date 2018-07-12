
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

    @property
    def size(self):
        return (self.w, self.h)

    def is_outside(self, x, y):
        return x >= self.w or y >= self.h or x < 0 or y < 0


class Coorded(object):
    x = 0
    y = 0


class Ball(Coorded):
    stage = None
    intensity = 1.0
    radius = 24.0

    def __init__(self, stage):
        self.stage = stage

    def rand_intensity(self, mini, maxi):
        self.intensity = random.random() * (maxi - mini) + mini
        return self

    def rand_rad(self, minr, maxr):
        self.radius = random.random() * (maxr - minr) + minr
        return self

    def rand_pos(self, size):
        self.x = random.randrange(0, size[0])
        self.y = random.randrange(0, size[1])
        return self

    def render(self):
        render_area = []

        x = self.x
        minx = math.floor(x - self.radius)
        maxx = math.ceil(x + self.radius)

        y = self.y
        miny = math.floor(y - self.radius)
        maxy = math.ceil(y + self.radius)

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
    return list(map(
        lambda ball:
            ball.rand_pos(stage.size)
                .rand_rad(5.0, 25.0)
                .rand_intensity(0.1, 1.0),
                [Ball(stage) for _ in range(count)]))

def main():
    stage = Stage()
    balls = []
    balls += rand_balls(stage, 1024)

    img = Image.new("RGBA", stage.size)
    pixels = img.load()
    for ball in balls:
        for px, py, v in ball.render():
            v2 = min(pixels[px, py][3] + int(v), 255)
            pixels[px, py] = (255, 255, 255, v2)

    img.save("res.png")


if __name__ == "__main__":
    main()
