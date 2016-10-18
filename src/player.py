"""
MediaPlayer plays the music files with omxplayer, and reacts to mouse-inputs
"""
import os
import subprocess
from random import shuffle

from logutils import setup_logger

logger = setup_logger()


# class PlayerThread()
class MediaPlayer(object):
    # filecollections is a list which contains lists of files to play.
    filecollections = []
    mix = []

    def __init__(self, basepath):
        self.filecollections = self.find_files(basepath)

    def find_files(self, basepath):
        path = os.path.abspath(basepath)

        # Get all top-level directories
        dirs = []
        for _path in os.listdir(path):
            _fullpath = os.path.join(path, _path)
            if os.path.isdir(_fullpath):
                dirs.append(_fullpath)
        # logger.info("albums: %s", dirs)

        # Collect all interesting files
        # filetypes = [".py", ".txt", ".md"]
        filetypes = [".mp3", ".aac", ".md"]
        filecollections = []  # this list contains lists of files for every base directory
        for dir in dirs:
            files = []
            for dirpath, dirnames, filenames in os.walk(dir):
                for f in filenames:
                    if os.path.splitext(f)[1].lower() in filetypes:
                        #print(os.path.join(dirpath, f))
                        files.append(os.path.join(dirpath, f))
            if files:
                filecollections.append(files)

        # Done
        return filecollections

    def start(self):
        # Now play the files of each child-list, and on mouse-click jump to random other child-list
        logger.info("START")
        while True:
            self.shuffle()

    def shuffle(self):
        # Shuffle Albums
        self.mix = self.filecollections[:]
        shuffle(self.mix)
        logger.info("shuffled new mix: %s", self.mix)

    def play_album(self, i):
        album = self.mix[i % len(self.mix)]
        for fn in album:
            self.play_file(fn)

    def play_file(self, fn):
        logger.info("play_file: %s" % fn)
        OMXPLAYER_SP_CMD = "omxplayer %s" % fn
        self.omx_process = subprocess.Popen(OMXPLAYER_SP_CMD, preexec_fn=os.setsid)
        logger.info('omxplayer PID is ' + str(self.omx_process.pid))
        logger.info("waiting for end of omxplayer...")
        self.omx_process.wait()
        logger.info("omxplayer finished")

    def kill_omxplayer(self):
        if self.omx_process and not self.omx_process.poll():
            # omxplayer is running... kill now by sending SIGTERM
            # to all children of the process groups
            logger.info("killing omxplayer with PID %s", str(self.omx_process.pid))
            try:
                os.killpg(os.getpgid(self.omx_process.pid), signal.SIGTERM)
            except Exception as e:
                logger.warn("could not kill omxplayer: %s", str(e))
