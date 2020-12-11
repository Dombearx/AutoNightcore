import nightcorer as nightcorer
import downloader as downloader

if __name__ == "__main__":

    downloader = downloader.Downloader()
    nightcorer = nightcorer.Nightcorer()
    
    urls = [
        "https://www.youtube.com/watch?v=nlt5Wa13fFU",
    ]

    downloader.download(urls)

    for filename in downloader.filenames:
        nightcorer.make_nightcore(filename)