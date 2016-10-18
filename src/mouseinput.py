import signal
from threading import Thread, Event


def wait_mouse_click():
    mouse = file('/dev/input/mice')
    while True:
        status, dx, dy = tuple(ord(c) for c in mouse.read(3))

        def to_signed(n):
            return n - ((0x80 & n) << 1)

        dx = to_signed(dx)
        dy = to_signed(dy)
        # print "status=%s / %#02x, %d, %d" % (status, status, dx, dy)
        if status in [9, 10, 12]:
            return


class MouseClickThread(Thread):
    def __init__(self, callback):
        Thread.__init__(self)
        self.daemon = True
        self.callback = callback
        self.stop_event = Event()

    def run(self):
        while not self.stop_event.is_set():
            # Continually wait for a mouse click
            wait_mouse_click()
            self.callback()


if __name__ == "__main__":
    # while True:
    #     wait_mouse_click()
    #     print "mouse clicked"
    def clicked():
        print "clicked"

    thread = MouseClickThread(clicked)
    thread.start()

    print "waiting for signal..."
    signal.pause()
    print "bye"
