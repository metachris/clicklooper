"""
Prerequisites:

* `sudo apt install python-pygame`

Info:

* https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
* Loading Indicator Sprite Generators:
  * http://preloaders.net/en/search/spinner
  * http://spiffygif.com/
"""
import os
import sys
import pygame
import time
import random

DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))

# os.environ["SDL_FBDEV"] = "/dev/fb0"
os.putenv('SDL_NOMOUSE', '1')

class FrameBuffer:
    screen = None
    size = None

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            print 'Using driver %s' % driver
            break

        if not found:
            raise Exception('No suitable video driver found!')

        pygame.mouse.set_visible(False)
        pygame.font.init()

        self.img_logo = pygame.image.load(os.path.join(DIR_SCRIPT, "images", "splash_trimmed.png"))

        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (self.size[0], self.size[1])
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        self.draw_splash_screen(self.screen)
        pygame.display.flip()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()

    def draw_splash_screen(self, surface):
        drawX = (self.size[0] / 2) - (self.img_logo.get_width() / 2)
        drawY = (self.size[1] / 2) - (self.img_logo.get_height() / 2) - 100
        surface.blit(self.img_logo, (drawX, drawY))

    def show_text(self, filename):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        # Add Logo
        self.draw_splash_screen(background)

        # Add first line of text
    	font = pygame.font.Font(None, 56)
    	text = font.render("Playing", 1, (114, 191, 68))
    	textpos = text.get_rect()
    	textpos.centerx = background.get_rect().centerx
    	textpos.y = self.size[1] - 220
    	background.blit(text, textpos)

        # Add second line of text
    	font = pygame.font.Font(None, 66)
    	text = font.render(filename, 1, (200, 200, 200))
    	textpos = text.get_rect()
    	textpos.centerx = background.get_rect().centerx
    	textpos.y = self.size[1] - 140
    	background.blit(text, textpos)

        # Update display
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

    def show_error(self, message):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        # Add Logo
        self.draw_splash_screen(background)

        # Add first line of text
    	font = pygame.font.Font(None, 66)
    	text = font.render(message, 1, (200, 0, 0))
    	textpos = text.get_rect()
    	textpos.centerx = background.get_rect().centerx
    	textpos.y = self.size[1] - 220
    	background.blit(text, textpos)

        # Update display
        self.screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    fb = FrameBuffer()
    # fb.test()
    # fb.show_text("Folder", "filename")
    fb.show_error("this is some error")
    time.sleep(10)
