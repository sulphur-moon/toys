# encoding:utf-8
import os
import sys
import time


class Screenshot(object):
    """docstring for Screenshot"""

    def __init__(self, filename='screenshot.png'):
        super(Screenshot, self).__init__()
        self.filename = filename

    def get_screenshot(self, rename='screenshot.png'):
        os.system('adb shell screencap -p /sdcard/{}'.format(self.filename))
        os.system('adb pull /sdcard/{} .'.format(self.filename))
        if rename != self.filename:
            os.rename(self.filename, rename)
        return rename


if __name__ == '__main__':
    screenshot = Screenshot()
    for i in range(322, 400):
        screenshot.get_screenshot(str(i) + '.png')
        print(i)
        time.sleep(2)
        os.system('adb shell input swipe 800 1000 400 1000')
        time.sleep(2)
