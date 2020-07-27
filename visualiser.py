import os
import sys
import numpy as np
import subprocess as sp
from PIL import Image, ImageDraw, ImageFont
import tempfile
from shutil import rmtree


def findFfmpeg():
    if sys.platform == "win32":
        return "ffmpeg.exe"
    else:
        try:
            with open(os.devnull, "w") as f:
                sp.check_call(['ffmpeg', '-version'], stdout=f, stderr=f)
            return "ffmpeg"
        except:
            return "avconv"


def readAudioFile(filename, FFMPEG_BIN):
    command = [FFMPEG_BIN,
               '-i', filename,
               '-f', 's16le',
               '-acodec', 'pcm_s16le',
               '-ar', '44100',  # ouput will have 44100 Hz
               '-ac', '1',  # mono (set to '2' for stereo)
               '-']

    in_pipe = sp.Popen(command, stdout=sp.PIPE,
                       stderr=sp.DEVNULL, bufsize=10**8)

    completeAudioArray = np.empty(0, dtype="int16")

    while True:
        # read 2 seconds of audio
        raw_audio = in_pipe.stdout.read(88200*4)
        if len(raw_audio) == 0:
            break
        audio_array = np.fromstring(raw_audio, dtype="int16")
        completeAudioArray = np.append(completeAudioArray, audio_array)
        # print(audio_array)

    in_pipe.kill()
    in_pipe.wait()

    # add 0s the end
    completeAudioArrayCopy = np.zeros(
        len(completeAudioArray) + 44100, dtype="int16")
    completeAudioArrayCopy[:len(completeAudioArray)] = completeAudioArray
    completeAudioArray = completeAudioArrayCopy

    return completeAudioArray


def drawBaseImage(backgroundFile, titleText="", titleFont="", fontSize="", alignment="",
                  xOffset="", yOffset="", textColor="", visColor=""):
    if backgroundFile == '':
        im = Image.new("RGB", (1920, 1080), "black")
    else:
        im = Image.open(backgroundFile)

    # resize if necessary
    if not im.size == (1920, 1080):
        im = im.resize((1920, 1080), Image.ANTIALIAS)

    return im

    '''
    self._image1 = QtGui.QImage(self._image)
    painter = QPainter(self._image1)

    font = titleFont
    font.setPixelSize(fontSize)
    painter.setFont(font)

    painter.setPen(QColor(*textColor))

    yPosition = yOffset

    fm = QtGui.QFontMetrics(font)
    if alignment == 0:      #Left
       xPosition = xOffset
    if alignment == 1:      #Middle
       xPosition = xOffset - fm.width(titleText)/2
    if alignment == 2:      #Right
       xPosition = xOffset - fm.width(titleText)
    painter.drawText(xPosition, yPosition, titleText)
    painter.end()

    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QIODevice.ReadWrite)
    self._image1.save(buffer, "PNG")

    strio = io.BytesIO()
    strio.write(buffer.data())
    buffer.close()
    strio.seek(0)

    return Image.open(strio)
    '''


def transformData(i, completeAudioArray, sampleSize, smoothConstantDown, smoothConstantUp, lastSpectrum):
    if len(completeAudioArray) < (i + sampleSize):
        sampleSize = len(completeAudioArray) - i

    window = np.hanning(sampleSize)
    data = completeAudioArray[i:i+sampleSize][::1] * window
    paddedSampleSize = 2048
    paddedData = np.pad(
        data, (0, paddedSampleSize - sampleSize), 'constant')
    spectrum = np.fft.fft(paddedData)
    sample_rate = 44100
    frequencies = np.fft.fftfreq(len(spectrum), 1./sample_rate)

    y = abs(spectrum[0:int(paddedSampleSize/2) - 1])

    # filter the noise away
    # y[y<80] = 0

    y = 20 * np.log10(y)
    y[np.isinf(y)] = 0

    if lastSpectrum is not None:
        lastSpectrum[y < lastSpectrum] = y[y < lastSpectrum] * smoothConstantDown + \
            lastSpectrum[y < lastSpectrum] * (1 - smoothConstantDown)
        lastSpectrum[y >= lastSpectrum] = y[y >= lastSpectrum] * \
            smoothConstantUp + lastSpectrum[y >=
                                            lastSpectrum] * (1 - smoothConstantUp)
    else:
        lastSpectrum = y

    # x = frequencies[0:int(paddedSampleSize/2) - 1]

    return lastSpectrum


def deleteTempDir(tempDir):
    if tempDir and os.path.exists(tempDir):
        rmtree(tempDir)


def getVideoFrames(videoPath, firstOnly=False):
    tempDir = os.path.join(tempfile.gettempdir(),
                           'visualizer-data')
    # recreate the temporary directory so it is empty
    deleteTempDir(tempDir)
    os.mkdir(tempDir)
    print("making:", tempDir)
    if firstOnly:
        filename = 'preview%s.jpg' % os.path.basename(
            videoPath).split('.', 1)[0]
        options = '-ss 10 -vframes 1'
    else:
        filename = '$frame%05d.jpg'
        options = ''
    sp.call(
        '%s -i "%s" -qscale:v 2 -y %s "%s"' % (
            FFMPEG_BIN,
            videoPath,
            options,
            os.path.join(tempDir, filename)
        ),
        shell=True
    )
    s = sorted([os.path.join(tempDir, f) for f in os.listdir(tempDir)])
    print("----")
    print(s)

    return s


def parseBaseImage(backgroundImage, preview=False):
    ''' determines if the base image is a single frame or list of frames '''
    if backgroundImage == "":
        return []
    else:
        _, bgExt = os.path.splitext(backgroundImage)
        if not bgExt == '.mp4':
            return [backgroundImage]
        else:
            return getVideoFrames(backgroundImage, preview)


def createVideo(backgroundImage, inputFile, outputFile):
    # print('worker thread id: {}'.format(QtCore.QThread.currentThreadId()))
    def getBackgroundAtIndex(i):
        return drawBaseImage(backgroundFrames[i])

    progressBarValue = 0

    # self.progressBarUpdate.emit(progressBarValue)
    # self.progressBarSetText.emit('Loading background image…')

    backgroundFrames = parseBaseImage(backgroundImage)
    print("---------")
    print(len(backgroundFrames))
    if len(backgroundFrames) < 2:
        # the base image is not a video so we can draw it now
        imBackground = getBackgroundAtIndex(0)
    else:
        # base images will be drawn while drawing the audio bars
        imBackground = None

    # self.progressBarSetText.emit('Loading audio file…')
    completeAudioArray = readAudioFile(inputFile, FFMPEG_BIN)

    # test if user has libfdk_aac
    encoders = sp.check_output(
        FFMPEG_BIN + " -encoders -hide_banner", shell=True)
    if b'libfdk_aac' in encoders:
        acodec = 'libfdk_aac'
    else:
        acodec = 'aac'

    ffmpegCommand = [FFMPEG_BIN,
                     # (optional) means overwrite the output file if it already exists.
                     '-y',
                     '-f', 'rawvideo',
                     '-vcodec', 'rawvideo',
                     '-s', '1920x1080',  # size of one frame
                     '-pix_fmt', 'rgb24',
                     '-r', '30',  # frames per second
                     '-i', '-',  # The input comes from a pipe
                     '-an',
                     '-i', inputFile,
                     '-acodec', acodec,  # output audio codec
                     '-b:a', "192k",
                     '-vcodec', "libx264",
                     '-pix_fmt', "yuv420p",
                     '-preset', "medium",
                     '-f', "mp4"]

    if acodec == 'aac':
        ffmpegCommand.append('-strict')
        ffmpegCommand.append('-2')

    ffmpegCommand.append(outputFile)

    out_pipe = sp.Popen(ffmpegCommand,
                        stdin=sp.PIPE, stdout=sys.stdout, stderr=sys.stdout)

    smoothConstantDown = 0.08
    smoothConstantUp = 0.8
    lastSpectrum = None
    sampleSize = 1470

    # np.seterr(divide='ignore')
    bgI = 0
    for i in range(0, len(completeAudioArray), sampleSize):
        # create video for output
        lastSpectrum = transformData(
            i,
            completeAudioArray,
            sampleSize,
            smoothConstantDown,
            smoothConstantUp,
            lastSpectrum)

        visColor = (255, 0, 0)
        if imBackground != None:
            im = drawBars(lastSpectrum, imBackground, visColor)
        else:
            im = drawBars(lastSpectrum, getBackgroundAtIndex(bgI), visColor)
            if bgI < len(backgroundFrames)-1:
                bgI += 1

        # write to out_pipe
        try:
            out_pipe.stdin.write(im.tobytes())
        finally:
            True

    #   # increase progress bar value
    #   if progressBarValue + 1 <= (i / len(completeAudioArray)) * 100:
    #     progressBarValue = numpy.floor((i / len(completeAudioArray)) * 100)
    #     self.progressBarUpdate.emit(progressBarValue)
    #     self.progressBarSetText.emit('%s%%' % str(int(progressBarValue)))

    np.seterr(all='print')

    out_pipe.stdin.close()
    if out_pipe.stderr is not None:
        print(out_pipe.stderr.read())
        out_pipe.stderr.close()
    # out_pipe.terminate() # don't terminate ffmpeg too early
    out_pipe.wait()
    print("Video file created")
    # self.core.deleteTempDir()
    # self.progressBarUpdate.emit(100)
    # self.progressBarSetText.emit('100%')
    # self.videoCreated.emit()


def drawBars(spectrum, image, color):

    imTop = Image.new("RGBA", (1920, 1080))
    draw = ImageDraw.Draw(imTop)

    color = (255, 255, 255)

    r, g, b = color
    color2 = (r, g, b, 50)

    backgroundBarsVerticalPos = 185
    barsVerticalPos = 180

    horizontalGap = 32

    backgroundLeftStart = 5
    # wewnętrzne są mniejsze, więc przesunięte o 5 dalej
    leftStart = 5 + backgroundLeftStart

    backgroundBarsPercentageOfForegroundBarXD = 20

    barHeight = 1

    barThiccness = 10
    backgroundBarThiccness = 20

    # max 1023 / 4 chyba
    numberOfBars = 63

    for j in range(0, numberOfBars):
        draw.rectangle((backgroundLeftStart + j * horizontalGap, backgroundBarsVerticalPos, backgroundLeftStart + j * horizontalGap + backgroundBarThiccness,
                        backgroundBarsVerticalPos - spectrum[j * 4] * barHeight - backgroundBarsPercentageOfForegroundBarXD), fill=color2)

        draw.rectangle((leftStart + j * horizontalGap, barsVerticalPos, leftStart + j * horizontalGap + barThiccness,
                        barsVerticalPos - spectrum[j * 4] * barHeight), fill=color)

    imBottom = imTop.transpose(Image.FLIP_TOP_BOTTOM)

    im = Image.new("RGB", (1920, 1080), "black")
    im.paste(image, (0, 0))
    im.paste(imTop, (0, 0), mask=imTop)
    im.paste(imBottom, (0, 0), mask=imBottom)

    return im


if __name__ == "__main__":
    FFMPEG_BIN = findFfmpeg()
    print(FFMPEG_BIN)

    FFMPEG_BIN = "ffmpeg"

    # audioFile = readAudioFile("piosenki/test.mp3", FFMPEG_BIN)

    # print(audioFile)
    # print(len(audioFile))
    # print(audioFile[400000])

    # im = parseBaseImage("images/background.jpg")

    # print(im)

    backgroundImage = "images/background.mp4"

    #backgroundImage = "images/background.jpg"
    inputFile = "piosenki/cutted.mp3"
    outputFile = "output/cutted.mp4"

    createVideo(backgroundImage, inputFile, outputFile)
