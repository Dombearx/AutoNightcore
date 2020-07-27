from PIL import Image
import numpy as np


def zoom_at(img, n):
    w, h = img.size

    left = 0
    top = 0
    right = w
    bottom = h

    img = img.crop((left + n, top + (n * 1.77),
                    right - n, bottom - n))

    return img.resize((w, h), Image.LANCZOS)


im = Image.open("./images/background.jpg")

im = zoom_at(im, 30)

im.show()
