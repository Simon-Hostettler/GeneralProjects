from PIL import Image
import sys
import os
import matplotlib.colors
import cProfile
import pstats
import io


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


current_path = sys.path[0]
if not os.path.exists(current_path + "/Images/"):
    os.makedirs(current_path + "/Images/")

# Settings for Image resolution
IMG_RATIO = 16/9
IMG_HEIGHT = 2160
IMG_WIDTH = int(IMG_RATIO * IMG_HEIGHT)

# Zoom and focal point functions, the smaller zoom is, the further out the image will be rendered
FOCAL_POINT = (0, 0)
ZOOM = 60
RANGE_X = (((-1.5*IMG_RATIO)/ZOOM) + FOCAL_POINT[0], (3.0*IMG_RATIO)/ZOOM)
RANGE_Y = ((-1.5/ZOOM) + FOCAL_POINT[1], 3.0/ZOOM)

# Settings for the Mandelbrot-function
ITERATIONS = 255
EXP_DEGREE = 2
ESCAPE_RADIUS = 2**EXP_DEGREE
JUL_CMPLX = complex(-0.4, 0.6)

# setting up a palette by creating a gradient between 3 colors, put any hex colors
matplotpalette = matplotlib.colors.LinearSegmentedColormap.from_list(
    "", [matplotlib.colors.to_rgb("#1a1a24"), matplotlib.colors.to_rgb("#b0afba"), matplotlib.colors.to_rgb("#00f2ff")], N=ITERATIONS+1)
palette = []
for i in range(ITERATIONS+1):
    matplotcolor = matplotlib.colors.to_rgb(
        matplotpalette((1/float(ITERATIONS))*i))
    color = (int(matplotcolor[0]*255), int(matplotcolor[1]*255), int(
        matplotcolor[2]*255))
    palette.append(color)
print(len(palette))

# calculates iterations of mb_function for the coordinates of each pixel and puts a color according to that


def draw_mandelbrot(width=1920, height=1080):
    img = Image.new('RGB', (width, height), color='white')
    for x in range(width):
        for y in range(height):
            cmplx = complex(
                RANGE_X[0] + x*(RANGE_X[1]/width),
                abs(RANGE_Y[0]) - y*(RANGE_Y[1]/height))
            iterations = mb_function(0, cmplx, 0)
            img.putpixel((x, y), palette[iterations])
        x % 100 == 0 and print(f"Column {x}/{width} is done")

    img.save(current_path + "/Images/Mandelbrot.png", quality=100)

# calculates iterations of mb_function according to the function f(z) = z**exp_degree + c for each pixel
# and puts a corresponding color


def draw_julia_set(img_num=0, width=1920, height=1080, jul_cmplx=complex(-0.4, 0.6)):
    img = Image.new('RGB', (width, height), color='white')
    for x in range(width):
        for y in range(height):
            cmplx = complex(
                RANGE_X[0] + x*(RANGE_X[1]/width),
                abs(RANGE_Y[0]) - y*(RANGE_Y[1]/height))
            iterations = mb_function(cmplx, jul_cmplx, 0)
            img.putpixel((x, y), palette[iterations])
        x % 100 == 0 and print(f"Column {x}/{width} is done")

    img.save(current_path + "/Images/Julia" +
             str(img_num) + ".png", quality=100)


'''to be ignored atm
def draw_julia_animation(img_height):
    height = img_height
    width = int(IMG_RATIO * height)
    steps = np.linspace(0, 2*math.pi, 100)
    for num, x in enumerate(steps):
        julcmplx = complex(0.7885*math.cos(x), 0.7885*math.sin(x))
        draw_julia_set(num, width, height, julcmplx)
'''


def mb_function(z, c, counter):
    while counter < ITERATIONS and abs(z) <= ESCAPE_RADIUS:
        z = z**EXP_DEGREE + c
        counter += 1
    return counter
    '''new_z = z**EXP_DEGREE + c
    if counter < ITERATIONS and abs(new_z) <= ESCAPE_RADIUS:
        return mb_function(new_z, c, counter+1)
    else:
        return counter'''


def main(dict):
    to_draw = "Julia"
    if(to_draw == "Julia"):
        draw_julia_set(0, IMG_WIDTH, IMG_HEIGHT, JUL_CMPLX)
    elif(to_draw == "MB"):
        draw_mandelbrot(IMG_WIDTH, IMG_HEIGHT)
    else:
        print(f"{to_draw} is not a valid option. Select MB or Julia.")


if __name__ == "__main__":
    main(dict())
