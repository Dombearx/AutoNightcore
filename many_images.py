# Improting Image class from PIL module
from PIL import Image
import numpy as np
# Opens a image in RGB mode
im = Image.open("./images/background.jpg")

# Size of the image in pixels (size of orginal image)
# (This is not mandatory)
width, height = im.size

print(width, height)

# Setting the points for cropped image
left = 200
top = 200
right = width - 200
bottom = height - 200

with open('moves.npy', 'rb') as f:

    moves = np.load(f)


print(moves)

index = 0

currentLeft = left
currentTop = top
currentRight = right
currentBottom = bottom

for move in moves:
    x, y = move
    im1 = im.crop((currentLeft + x, currentTop + y,
                   currentRight + x, currentBottom + y))

    currentLeft = currentLeft + x
    currentTop = currentTop + y
    currentRight = currentRight + x
    currentBottom = currentBottom + y

    im1.save("./animation/" + str(index) + ".jpg")

    index += 1
# Cropped image of above dimension
# (It will not change orginal image)
# for i in range(100):

#     im1 = im.crop((left - i, top, right - i, bottom))

#     im1.save("./animation/" + str(i) + ".jpg")

# for i in range(100, 0, -1):

#     im1 = im.crop((left - i, top, right - i, bottom))

#     im1.save("./animation/" + str(100 + (100 - i)) + ".jpg")
# Shows the image in image viewer
# im1.show()
