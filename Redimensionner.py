from PIL import Image

class Redimensionner(object):
    def __init__(self,name):
        self.img = Image.open(name + ".png").convert("RGBA")
        self.width = self.img.size[0]
        self.height = self.img.size[1]

    """def background_transparent(self,t=50):
        R, G, B, A = self.img.getpixel((0, 0))
        for x in range(self.width):
            for y in range(self.height):
                r, g, b, a = self.img.getpixel((x, y))
                if R - t <= r <= R + t and G - t <= g <= G + t and B - t <= b <= B + t or a == 0:
                    self.img.putpixel((x, y), (50, 50, 50, 0))
        self.img.show()"""

    def transparent(self,t=50):
        blank = [(0, 0)]
        unknown = []
        for large in range(self.width):
            for tall in range(self.height):
                unknown.append((large,tall))
        while unknown:
            x = blank[0][0]
            y = blank[0][1]
            r, g, b, a = self.img.getpixel((x,y))
            if (x + 1, y) in blank and self.condition_pixel_est_invisible(x,y,t) == True:
                self.img.putpixel((x,y), (50, 50, 50, 0))
                blank.append((x + 1, y))
            elif (x - 1, y) in blank  and self.condition_pixel_est_invisible(x,y,t) == True:
                self.img.putpixel((x,y), (50, 50, 50, 0))
                blank.append((x - 1, y))
            elif (x ,y + 1) in blank  and self.condition_pixel_est_invisible(x,y,t) == True:
                self.img.putpixel((x,y), (50, 50, 50, 0))
                blank.append((x ,y + 1))
            elif (x, y - 1) in blank  and self.condition_pixel_est_invisible(x,y,t) == True:
                self.img.putpixel((x, y), (50, 50, 50, 0))
                blank.append((x, y - 1))
                print(blank[0][0]+1)
            else:
                blank.remove(blank[0])
                print((x + 1,y),r, g, b, a)
                print((x - 1,y),r, g, b, a)
                print((y + 1, x),r, g, b, a)
                print((y - 1, x),r, g, b, a)
                print("else","\n")
            print(blank)
        self.img.show()

    def condition_pixel_est_invisible(self,x,y,t):
        R, G, B, A = self.img.getpixel((0, 0))
        r, g, b, a = self.img.getpixel((x, y))
        if R - t <= r <= R + t and G - t <= g <= G + t and B - t <= b <= B + t or a == 0:
            print("True")
            return True
        print("False")
        return False