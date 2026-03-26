from Redimensionner import Redimensionner

if __name__ == '__main__':
    #img = (Redimensionner("test1"))
    #img.background_transparent()
    img = (Redimensionner("test1"))
    img.condition_pixel_est_invisible(0,0,50)
    img.transparent()