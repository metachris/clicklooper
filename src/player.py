"""
MediaPlayer plays the music files with omxplayer, and reacts to mouse-inputs
"""
import os
import time
import subprocess
import signal
from random import shuffle
from threading import Thread, Event

from mouseinput import wait_mouse_click, MouseClickThread
from logutils import setup_logger

logger = setup_logger()

class MixPlaybackThread(Thread):
    mix = []
    album_last = None

    def __init__(self, filecollections):
        Thread.__init__(self)
        self.daemon = True
        self.event_quit = Event()
        self.event_mouse = Event()
        self.filecollections = filecollections

    def shutdown(self):
        self.event_quit.set()
        self.kill_omxplayer()

    def mouse_clicked(self):
        logger.info("mouse was clicked")
        self.event_mouse.set()
        self.kill_omxplayer()

    def create_mix(self):
        # Shuffle Albums
        self.mix = self.filecollections[:]
        shuffle(self.mix)
        logger.info("shuffled new mix: %s", self.mix)
        if self.mix[0] == self.album_last and len(self.mix) > 1:
            self.mix.pop(0)
            logger.info("- removed first album of new mix, because its just been played")

    def run(self):
        logger.info("Starting album playback...")
        while not self.event_quit.is_set():
            # Perhaps re-shuffle albums
            if not self.mix:
                self.create_mix()

            # Now play the next album
            album = self.mix.pop(0)
            self.play_album(album)

    def play_album(self, album):
        logger.info("playing album %s", album)
        self.album_last = album
        for fn in album:
            if self.event_mouse.is_set() or self.event_quit.is_set():
                self.event_mouse.clear()
                return
            self.play_file(fn)

    def play_file(self, fn):
        logger.info("play_file: %s" % fn)
        OMXPLAYER_SP_CMD = ['omxplayer', '-o', 'both', fn]
        logger.debug(OMXPLAYER_SP_CMD)
        # OMXPLAYER_SP_CMD = ["sleep", "2"]
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


class MediaPlayer(object):
    # filecollections is a list which contains lists of files to play.
    filecollections = []
    event_mouse = None
    event_quit = None
    mouse_thread = None
    player_thread = None

    def __init__(self, basepath):
        self.filecollections = self._find_files(basepath)
        self.mix = []
        self.current_album = 0
        self.event_mouse = Event()
        self.event_quit = Event()

    def _find_files(self, basepath):
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

    def start_playback(self):
        # Now play the files of each child-list, and on mouse-click jump to random other child-list
        self.player_thread = MixPlaybackThread(self.filecollections)
        self.player_thread.start()

        self.mouse_thread = MouseClickThread(self.player_thread.mouse_clicked)
        self.mouse_thread.start()

        logger.info("threads started. waiting for quit signal...")
        # signal.signal(signal.SIGINT, self.shutdown)
        # print 'Press Ctrl+C'
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.player_thread.shutdown()
            time.sleep(1)

        logger.info("bye")
