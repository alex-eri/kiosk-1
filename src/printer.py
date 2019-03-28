import escpos.printer
import time
import logging
from escpos.constants import RT_STATUS_ONLINE, GS
from escpos.image import EscposImage

def retry(fu):
    def inner(self, *a, **kw):
        try:
            return fu(self, *a, **kw)
        except Exception as e:
            logging.error(repr(e))
            self.printer.device.reset()
            time.sleep(2)
            self.printer.open()
        try:
            return fu(self, *a, **kw)
        except Exception as e:
            logging.error(repr(e))
            raise e

    return inner


class Printer:

    def __init__(self, file=None, usb=[], *a, **kw):
        self.file = file
        self.usb = usb

        if self.file:
            self.printer = escpos.printer.File(self.file)

        elif self.usb.get('idVendor'):
            self.printer = escpos.printer.Usb(**self.usb)

    def open(self):
        self.printer.open()

    def wait(self):
        while not(self.printer.is_online()):
            time.sleep(0.2)

    #@retry
    def print(self, img):
        self.printer._raw(GS+b'\xf6')
        time.sleep(0.2)
        self.printer.image(img)

    #@retry
    def cut(self):
        self.printer._raw(GS+b'\xf8')
        time.sleep(0.2)
        self.printer.cut(feed=False)




'''
p._raw(b'\x1d\xf6')
p.image(imgr)
p._raw(b'\x1d\xf8')
p.cut(feed=False)
p._raw(b'\x1d\xf6')
p.image(imgr)
p._raw(b'\x1d\xf8')
p.cut(feed=False)
'''
