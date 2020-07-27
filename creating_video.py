from moviepy.editor import *


myclip = ImageClip("./images/background.jpg", duration=20)

myclip.write_videofile("./output/movie.mp4", fps=15)
# myclip = ImageClip(somme_array)  # a (height x width x 3) RGB numpy array
# myclip = some_video_clip.to_ImageClip(t='01:00:00')  # frame at t=1 hour.


# Testowy komentarz sluzacy testom
