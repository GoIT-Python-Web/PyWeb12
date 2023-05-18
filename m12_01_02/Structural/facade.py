class VideoFile:
    def __init__(self, filename):
        self.filename = filename

    def decode(self):
        print(f"Decoding video file {self.filename}")


class AudioFile:
    def __init__(self, filename):
        self.filename = filename

    def decode(self):
        print(f"Decoding audio file {self.filename}")


class SubtitlesFile:
    def __init__(self, filename):
        self.filename = filename

    def add(self):
        print(f"Add subtitles {self.filename}")


class VideoPlayer:
    def __init__(self, video_file: VideoFile, audio_file: AudioFile, sub: SubtitlesFile):
        self.video_file = video_file
        self.audio_file = audio_file
        self.sub = sub

    def play(self):
        self.video_file.decode()
        self.audio_file.decode()
        self.sub.add()


if __name__ == '__main__':
    video_file = VideoFile('my_summer.mp4')
    audio_file = AudioFile('my_summer.mp3')
    sub_file = SubtitlesFile('my_summer.srt')

    player = VideoPlayer(video_file, audio_file, sub_file)
    player.play()
