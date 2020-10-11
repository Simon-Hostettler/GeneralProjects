from PIL import Image, ImageColor
from palette import palette
import sys

current_path = sys.path[0]
MBorJulia = {"MB": 1, "Julia": 0}

IMG_RATIO = 16/9
IMG_HEIGHT = 1000
IMG_WIDTH = int(IMG_RATIO * IMG_HEIGHT)

RANGE_X = (-1.5*IMG_RATIO, 3.0*IMG_RATIO)
RANGE_Y = (-1.5, 3.0)

ITERATIONS = 255
JUL_CMPLX = complex(0.285, 0.01)

for i in range(len(palette)):
    palette[i] = ImageColor.getrgb(palette[i])


def draw_mandelbrot():
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color='white')
    for x in range(IMG_WIDTH):
        for y in range(IMG_HEIGHT):
            cmplx = complex(
                RANGE_X[0] + x*(RANGE_X[1]/IMG_WIDTH),
                abs(RANGE_Y[0]) - y*(RANGE_Y[1]/IMG_HEIGHT))
            iterations = mb_function(0, cmplx, 0)
            img.putpixel((x, y), palette[iterations])
        x % 100 == 0 and print(f"Column {x} is done")

    img.save(current_path + "\\Images\\Mandelbrot.png", quality=100)


def draw_julia_set():
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color='white')
    for x in range(IMG_WIDTH):
        for y in range(IMG_HEIGHT):
            cmplx = complex(
                RANGE_X[0] + x*(RANGE_X[1]/IMG_WIDTH),
                abs(RANGE_Y[0]) - y*(RANGE_Y[1]/IMG_HEIGHT))
            iterations = mb_function(cmplx, JUL_CMPLX, 0)
            img.putpixel((x, y), palette[iterations])
        x % 100 == 0 and print(f"Column {x} is done")

    img.save(current_path + "\\Images\\Julia.png", quality=100)


def mb_function(z, c, counter):
    new_z = z*z + c
    if counter < ITERATIONS and abs(new_z) <= 4:
        return mb_function(new_z, c, counter+1)
    else:
        return counter


if __name__ == "__main__":
    select_set_to_draw = "Julia"
    if(MBorJulia[select_set_to_draw]):
        draw_mandelbrot()
    else:
        draw_julia_set()
