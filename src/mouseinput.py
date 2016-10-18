mouse = file('/dev/input/mice')

def wait_mouse_click():
    while True:
        status, dx, dy = tuple(ord(c) for c in mouse.read(3))

        def to_signed(n):
            return n - ((0x80 &amp; n) &lt;&lt; 1)

        dx = to_signed(dx)
        dy = to_signed(dy)
        print "%#02x %d %d" % (status, dx, dy)
        if status in ["0x9", "0xa", "0xc"]:
            return

while True:
    wait_mouse_click()
    print "mouse clicked"
