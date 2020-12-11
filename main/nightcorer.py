import nightcore as nc
import os 
from os import path

#rewritten Mariusz's nightcore_maker
class Nightcorer:

    def __init__(self):

        self.config = {
            # Nowy przyrowstek do nazwy utworu 
            "new_name_prefix" : "nightcored_",
            # Format audio
            "audio_format" : ".mp3",
            # Speed w procentach 
            "song_speed" : 110,
            # Peach 
            "song_tones" : 1,
            # Semi_tones ? 
            "song_semitones" : 0,
            # Octaves ? 
            "song_octaves" : 0,
        }
    
    def make_nightcore(self, song_name):
        new_song_name = self.config["new_name_prefix"] + song_name[:-4] + self.config["audio_format"]

        nc_audio = nc.nightcore(song_name, nc.Percent(self.config["song_speed"]))
        nc_audio = nc.nightcore(nc_audio, nc.Tones(self.config["song_tones"]))
        nc_audio = nc.nightcore(nc_audio, nc.Semitones(self.config["song_semitones"]))
        nc_audio = nc.nightcore(nc_audio, nc.Octaves(self.config["song_octaves"]))

        # Export gotowego audio 
        nc_audio.export(new_song_name)

#You should never call main fucntion unless it's for testing.
if __name__ == "__main__":

    nightcorer = Nightcorer()    
    
    filenames = ["With Extreme Prejudice-EK8IeNmGuIQ.mp3"]

    for filename in filenames:
        print(filename)
        nightcorer.make_nightcore(filename)