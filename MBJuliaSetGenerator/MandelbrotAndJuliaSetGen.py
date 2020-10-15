from PIL import Image
import sys
import matplotlib.colors

current_path = sys.path[0]

IMG_RATIO = 16/9
IMG_HEIGHT = 2160
IMG_WIDTH = int(IMG_RATIO * IMG_HEIGHT)

FOCAL_POINT = (0, 0)
ZOOM = 1
RANGE_X = (((-1.5*IMG_RATIO)/ZOOM) + FOCAL_POINT[0], (3.0*IMG_RATIO)/ZOOM)
RANGE_Y = ((-1.5/ZOOM) + FOCAL_POINT[1], 3.0/ZOOM)

ITERATIONS = 255
EXP_DEGREE = 2
ESCAPE_RADIUS = 2**EXP_DEGREE
JUL_CMPLX = complex(-0.4, 0.6)

matplotpalette = matplotlib.colors.LinearSegmentedColormap.from_list(
    "", [matplotlib.colors.to_rgb("#000020"), "yellow", "firebrick"], N=256)
palette = []
for i in range(ITERATIONS+1):
    matplotcolor = matplotlib.colors.to_rgb(matplotpalette((1/255.0)*i))
    color = (int(matplotcolor[0]*255), int(matplotcolor[1]*255), int(
                matplotcolor[2]*255))
    palette.append(color)


def draw_mandelbrot():
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color='white')
    for x in range(IMG_WIDTH):
        for y in range(IMG_HEIGHT):
            cmplx = complex(
                RANGE_X[0] + x*(RANGE_X[1]/IMG_WIDTH),
                abs(RANGE_Y[0]) - y*(RANGE_Y[1]/IMG_HEIGHT))
            iterations = mb_function(0, cmplx, 0)
            img.putpixel((x, y), palette[iterations])
        x % 100 == 0 and print(f"Column {x}/{IMG_WIDTH} is done")

    img.save(current_path + "/Images/Mandelbrot.png", quality=100)


def draw_julia_set():
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color='white')
    for x in range(IMG_WIDTH):
        for y in range(IMG_HEIGHT):
            cmplx = complex(
                RANGE_X[0] + x*(RANGE_X[1]/IMG_WIDTH),
                abs(RANGE_Y[0]) - y*(RANGE_Y[1]/IMG_HEIGHT))
            iterations = mb_function(cmplx, JUL_CMPLX, 0)
            img.putpixel((x, y), palette[iterations])
        x % 100 == 0 and print(f"Column {x}/{IMG_WIDTH} is done")

    img.save(current_path + "/Images/Julia.png", quality=100)


def mb_function(z, c, counter):
    new_z = z**EXP_DEGREE + c
    if counter < ITERATIONS and abs(new_z) <= ESCAPE_RADIUS:
        return mb_function(new_z, c, counter+1)
    else:
        return counter


if __name__ == "__main__":
    select_set_to_draw = "Julia"
    if(select_set_to_draw == "MB"):
        draw_mandelbrot()
    else:
        draw_julia_set()
