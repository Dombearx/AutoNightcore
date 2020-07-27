import os
import glob
from natsort import natsorted
from moviepy.editor import *
import cv2
import pprint as pp
import numpy as np

base_dir = os.path.realpath("./animation")
print(base_dir)


gif_name = 'pic'
fps = 60

# Get all the pngs in the current directory
file_list = glob.glob(base_dir + '/*.jpg')
file_list_sorted = natsorted(file_list, reverse=False)  # Sort the images

clips = [ImageClip(m).set_duration(1/fps)
         for m in file_list_sorted]

print(clips)
concat_clip = concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile("test.mp4", fps=fps)
