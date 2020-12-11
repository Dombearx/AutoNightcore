from __future__ import unicode_literals
import youtube_dl
import pprint as pp
import os.path

class Downloader:

    def __init__(self):

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            '-v': True,
            'print_json': True,
            'getfilename': '--get-filename',
            '--get-filename': True,
            '-e': True,
        }
        
        self.downloader = youtube_dl.YoutubeDL(self.ydl_opts) 

    def download(self, urls):

        self.filenames = []

        for url in urls:
            filename = self._download_one_song(url)

            self.filenames.append(filename)

    def _download_one_song(self, url):

        info = self.downloader.extract_info(url, download=False)

        filename  = info["title"] + "-" + url.split("=")[1] + ".mp3"

        if not os.path.isfile(filename):
            self.downloader.download([url,])
            
        return filename

#You should never call main fucntion unless it's for testing.
if __name__ == "__main__":

    downloader = Downloader()

    urls = [
        "https://www.youtube.com/watch?v=EK8IeNmGuIQ",
        #"https://www.youtube.com/watch?v=FYmm5YQSv2I",
    ]
    
    downloader.download(urls)
    print(downloader.filenames)