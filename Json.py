import json
from PIL import Image

class Json:

    def __init__(self, img):
        self.img = Image.open(img)
        self.nom = img

    def save_pixels(self):
        all_pixels = list(self.img.getdata())
        width, height = self.img.size
        grid = []

        for y in range(height):
            row = []
            for x in range(width):
                row.append(all_pixels[y * width + x])
            grid.append(row)

        data = {
            "larg": width,
            "haut": height,
            "pixel": grid
        }

        with open(f"{self.nom}.json", "w", encoding="utf-8") as f:
            f.write(f'{{"larg": {width}, "haut": {height}, "pixel": [\n')
            for i, row in enumerate(grid):
                virgule = "," if i < height - 1 else ""
                f.write(f'  {json.dumps(row)}{virgule}\n')
            f.write(']}')

if __name__ == "__main__":
    perso = Json("test.png")
    perso.save_pixels()