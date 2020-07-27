import os
import glob
from natsort import natsorted
from moviepy.editor import *
import cv2
import pprint as pp
import numpy as np

base_dir = os.path.realpath("./animation")
print(base_dir)

im = cv2.imread("pattern2.png")

# pp.pprint(im)
# Jest BGR bo czemu nie

usedPixels = []


def checkNeighbours(im, coords):

    diagonal_neighbours = []
    neighbours = []

    x = [-1, 1]
    y = [-1, 1]

    currentX, currentY = coords

    for xVal in x:
        for yVal in y:
            try:
                color = im[currentX + xVal, currentY + yVal]
                diagonal_neighbours.append(
                    (color, currentX + xVal, currentY + yVal))
            except:
                pass

    for yVal in y:
        try:
            color = im[currentX, currentY + yVal]
            neighbours.append(
                (color, currentX, currentY + yVal))
        except:
            pass

    for xVal in x:
        try:
            color = im[currentX + xVal, currentY]
            neighbours.append(
                (color, currentX + xVal, currentY))
        except:
            pass

    return diagonal_neighbours, neighbours


print(np.array([255, 255, 255]))
for rowIndex, row in enumerate(im):
    for index, pixel in enumerate(row):
        if not (pixel == [255, 255, 255]).all() and not (pixel == [0, 0, 0]).all():
            print(pixel, rowIndex, index)
            if pixel[2] > pixel[0] and pixel[2] > pixel[1]:
                # RED
                redEnd = (rowIndex, index)
            if pixel[1] > pixel[0] and pixel[1] > pixel[2]:
                # Green
                greenStart = (rowIndex, index)

print(redEnd)
print(greenStart)


currentCords = greenStart


def tupleInTuple(tupleToFound, listOfTuples):
    for t in listOfTuples:
        if t[1:] == tupleToFound[1:]:
            return True
        # for x1, x2 in zip(t[1:], tupleToFound[1:]):
        #     if x1 != x2:
        #         break
        # else:
        #     return True

    return False


moves = []
index = 0
while(currentCords != redEnd and index < 1000):
    diagonal_neighbours, neighbours = checkNeighbours(im, currentCords)
    #index += 1
    print("currentCords", currentCords)
    # input()
    foundNext = False

    for neighbour in neighbours:
        if (neighbour[0] == [0, 0, 0]).all():
            if not tupleInTuple(neighbour, usedPixels):
                usedPixels.append(neighbour)
                neighbourCoords = neighbour[1:]
                print("if1")
                moves.append(np.subtract(neighbourCoords, currentCords))

                currentCords = neighbourCoords
                foundNext = True
                break

    if(not foundNext):
        for neighbour in diagonal_neighbours:
            if (neighbour[0] == [0, 0, 0]).all():
                if not tupleInTuple(neighbour, usedPixels):
                    usedPixels.append(neighbour)
                    neighbourCoords = neighbour[1:]
                    print("if3")
                    moves.append(np.subtract(neighbourCoords, currentCords))

                    currentCords = neighbourCoords
                    foundNext = True
                    break

    if(not foundNext):
        for neighbour in neighbours:
            # find end
            if not (neighbour[0] == [255, 255, 255]).all():
                if not tupleInTuple(neighbour, usedPixels):
                    usedPixels.append(neighbour)
                    neighbourCoords = neighbour[1:]
                    print("if2")
                    moves.append(np.subtract(neighbourCoords, currentCords))

                    currentCords = neighbourCoords
                    foundNext = True
                    break

    if(not foundNext):
        for neighbour in diagonal_neighbours:
            # find end
            if not (neighbour[0] == [255, 255, 255]).all():
                if not tupleInTuple(neighbour, usedPixels):
                    usedPixels.append(neighbour)
                    neighbourCoords = neighbour[1:]
                    print("if4")
                    moves.append(np.subtract(neighbourCoords, currentCords))

                    currentCords = neighbourCoords
                    foundNext = True
                    break


print(diagonal_neighbours)

print(neighbours)

pp.pprint(moves)

with open('moves.npy', 'wb') as f:
    np.save(f, moves)
# gif_name = 'pic'
# fps = 60

# # Get all the pngs in the current directory
# file_list = glob.glob(base_dir + '/*.jpg')
# file_list_sorted = natsorted(file_list, reverse=False)  # Sort the images

# clips = [ImageClip(m).set_duration(1/fps)
#          for m in file_list_sorted]

# print(clips)
# concat_clip = concatenate_videoclips(clips, method="compose")
# concat_clip.write_videofile("test.mp4", fps=fps)
