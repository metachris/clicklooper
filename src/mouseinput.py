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

if __name__ == "__main__":
    while True:
        wait_mouse_click()
        print "mouse clicked"
