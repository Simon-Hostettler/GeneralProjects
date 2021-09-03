from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np
import sys

GSCALE = "@%#*+=-:. "
# GSCALE = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
ASCII_HEIGHT = 50
SAVE_FILE = "ascii.txt"
ROW_TO_COL_RATIO = 2.3


def convert_to_ascii(filename):
    img = Image.open(filename)
    gray_img = img.convert('L')
    w, h = img.size
    img_ratio = w/h
    downscaled_img = gray_img.resize(
        (int(ASCII_HEIGHT*img_ratio*ROW_TO_COL_RATIO), ASCII_HEIGHT))
    pixels = np.array(downscaled_img)

    with open(SAVE_FILE, "w") as file:
        for row in range(0, ASCII_HEIGHT):
            line = ""
            for column in range(0, int(ASCII_HEIGHT*img_ratio*ROW_TO_COL_RATIO)):
                gray_val = pixels[row][column]
                ascii_num = int(gray_val/255*(len(GSCALE)-1))
                line += GSCALE[ascii_num]
            file.write(line + "\n")


if __name__ == "__main__":
    image_name = askopenfilename()
    convert_to_ascii(image_name)
