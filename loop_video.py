from moviepy.editor import VideoFileClip, concatenate_videoclips
clip1 = VideoFileClip("output.mp4")


final_clip = concatenate_videoclips([clip1, clip1, clip1])

final_clip.write_videofile("my_concatenation.mp4")
