from PIL import Image
from collections import deque


class Background(object):
    def __init__(self, name):
        self.img = Image.open(name + ".png").convert("RGBA").copy()
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        self.fond = self.img.getpixel((0, 0))

    def transparent(self, start_x=0, start_y=0, t=50):
        self.fond = self.img.getpixel((start_x, start_y))
        blank = deque()
        blank.append((start_x, start_y))
        visited = set()
        visited.add((start_x, start_y))

        while blank:
            x, y = blank.popleft()

            if self.condition_pixel_est_invisible(x, y, t):
                self.img.putpixel((x, y), (50, 50, 50, 0))
                for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if (nx, ny) not in visited and 0 <= nx < self.width and 0 <= ny < self.height:
                        visited.add((nx, ny))
                        blank.append((nx, ny))
            else:
                visited.add((x, y))

    def condition_pixel_est_invisible(self, x, y, t):
        R, G, B, A = self.fond
        r, g, b, a = self.img.getpixel((x, y))
        if (R - t <= r <= R + t and G - t <= g <= G + t and B - t <= b <= B + t) or a == 0:
            return True
        return False

    def save(self, name):
        self.img.save(name + ".png")

    def show(self):
        self.img.show()