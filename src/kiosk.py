import sys
import random
import os
import os.path
import time
import json
import urllib.request
import urllib.error
import logging
import subprocess
import shlex

from util import retry
import threading

try:
    from PySide2 import QtGui
    from PySide2 import QtQml
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtWebEngine
    from PySide2.QtCore import QObject, Signal, Slot, Property
    import content.resource

except ImportError:
    DEPS = ['PySide2']
    CMD = 'install --user --timeout 120 ' + " ".join(DEPS)
    try:
        import pip
        pip.main(CMD.split())
    except:
        import pip._internal
        pip._internal.main(CMD.split())
    sys.exit(302)

try:
    import yaml
    from printercontroller import printController

except ImportError:
    DEPS = ['python-escpos==3.0a4', 'CairoSVG', 'python-libinput==0.3.0a']
    CMD = 'install --user --timeout 120 ' + " ".join(DEPS)
    try:
        import pip
        pip.main(CMD.split())
    except:
        import pip._internal
        pip._internal.main(CMD.split())
    sys.exit(302)

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


num1 = 49
mum2 = 53

class Checker(threading.Thread):
    __cb = [None]

    def __init__(self, timeout, cb, *a, **kw):
        super().__init__(*a, **kw)
        self.timeout = timeout
        self.__cb[0] = cb
        self.daemon = True

    def run(self):
        time.sleep(self.timeout * 60)
        self.__cb[0]()


class settingsController(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.settings = {}
        self._system_id = None
        self.touch_id = None
        self._n = 0
        self.x0 = 0
        self.x1 = 0
        self.y0 = 0
        self.y1 = 0
        self.raw_x = 0
        self.raw_y = 0
        self._x = 0
        self._y = 0
        self.checker = None

    def while_touch(self):
        from libinput import LibInput, ContextType, EventType
        li = LibInput(context_type=ContextType.UDEV)
        li.assign_seat('seat0')
        for e in li.events:
            if e.type == EventType.POINTER_MOTION_ABSOLUTE:
                #print(e.absolute_coords)
                self.raw_x, self.raw_y = e.absolute_coords
            if e.type == EventType.POINTER_MOTION_ABSOLUTE:
                self._x, self._y = e.transform_absolute_coords(1024, 768)

    @Slot()
    def touch(self):
        print((self.raw_x, self.raw_y ))
        if self._n == 0:
            self.x0 = self._x
            self.y0 = self._y
            self.x1 = 0
            self.y1 = 0
            self._n = 1
        elif self._n == 1:
            self.y0 = (self.y0+self._y)/2
            self.x1 = self._x
            self._n = 2
        elif self._n == 2:
            self.x0 = (self.x0+self._x)/2
            self.y1 = self._y
            self._n = 3
        elif self._n == 3:
            self.x1 = (self.x1 + self._x)/2
            self.y1 = (self.y1 + self._y)/2
            self._n = 4
        elif self._n == 4:
            self.calibrate()
            self._n = 5
        print(self._n)
        self.n_changed.emit()


    n_changed= Signal()

    @Property(int, notify=n_changed)
    def n(self):
        return self._n

    @retry(urllib.error.URLError)
    def load(self):
        url = "https://kiosk.multidat.ru/configs/%s.json" % self.system_id
        print(url)
        cfg = urllib.request.urlopen(url, timeout=5).read()
        self.settings = yaml.load(cfg)
        local_settings = {}
        try:
            with open(os.path.expanduser('~/.config/kiosk.yaml'),'r') as f:
                local_settings = yaml.load(f.read())
        except FileNotFoundError:
            local_settings = {}

        local_settings.pop('api', None)
        for k in local_settings:
            if self.settings.get(k) and isinstance(self.settings[k], dict):
                self.settings[k].update(local_settings[k])
            else:
                self.settings[k] = local_settings[k]

        self.local_settings = local_settings

        matrix = self.settings.get('touch', {}).get(
            'matrix',
            [1, 0, 0, 0, 1, 0, 0, 0, 1]
            )
        if self.settings.get('touch'):
            self.recalibrate(matrix)

    def get_touch_id(self):
        cmd = 'xinput list --id-only "%s"' % self.settings.get('touch',{}).get('name', 'QEMU QEMU USB Tablet')
        cmd = shlex.split(cmd)
        with subprocess.Popen(cmd, stdout=subprocess.PIPE) as p:
            touch_id = p.stdout.read().strip()
            if touch_id.isdigit():
                self.touch_id = int(touch_id)
                logging.info('Touch ID %d' % self.touch_id)

    @Slot()
    def calibrateresetdefault(self):
        self.recalibrate([1, 0, 0, 0, 1, 0, 0, 0, 1])

    @Slot()
    def calibrateresetsaved(self):
        self.recalibrate(self.matrix)

    def recalibrate(self, matrix):
        self.get_touch_id()
        if self.touch_id:
            m = " ".join(map(lambda x: "%.6f" % x, matrix))
            cmd = 'xinput set-float-prop %d "Coordinate Transformation Matrix" %s' %  (self.touch_id, m)
            cmd = shlex.split(cmd)
            subprocess.run(cmd)
            self.matrix = matrix
        self._n = 0
        self.n_changed.emit()

    def calibrate(self, w=1024, h=768):
        a0, b0, c0, d0, e0, f0, g0, h0, i0 = self.matrix

        x0,y0,x1,y1 = self.x0,self.y0,self.x1,self.y1

        a1 = 6*w/8/(x1-x0)
        c1 = (w/8-a1*x0)/w
        e1 = 6*h/8/(y1-y0)
        f1 = (h/8-e1*y0)/h
        """
        print((a1, e1))

        print(self.matrix)
        a = a1*a0
        e = e1*e0
        c = (c0/a0 + c1/a1) * a
        f = (f0/e0 + f1/e1) * e
        """
        matrix = [a1, b0, c1, d0, e1, f1, g0, h0, i0]
        logging.info(matrix)
        print(matrix)
        self.recalibrate(matrix)

    @Slot()
    def calibratesave(self):
        logging.basicConfig(level=logging.INFO)
        logging.info('saving')
        if not self.local_settings.get('touch'):
            self.local_settings['touch'] = {}
        self.local_settings['touch'].update({
                'name': self.settings.get('touch', {}).get('name', 'QEMU QEMU USB Tablet'),
                'matrix': self.matrix
            })
        self.settings['touch'].update(self.local_settings['touch'])

        self.save_local_settings()
        self._n = 0
        self.n_changed.emit()

    def save_local_settings(self):
        with open(os.path.expanduser('~/.config/kiosk.yaml'), 'w') as f:
            f.write(yaml.dump(self.local_settings))

    settings_changed = Signal()

    @Property(str, notify=settings_changed)
    def title(self):
        return self.settings['kiosk'].get('title', 'Билеты')

    @Property(str, notify=settings_changed)
    def color(self):
        return self.settings['kiosk'].get('color', 'white')

    @Property(str, notify=settings_changed)
    def apikey(self):
        return self.settings['api'].get('key', '876543210')

    @Property(str, notify=settings_changed)
    def apiurl(self):
        return self.settings['api'].get('url', 'https://kiosk.multidat.ru/api')

    @Property(str, notify=settings_changed)
    def help(self):
        return self.settings['kiosk'].get('help', 'http://www.multidat.ru/продукты/мультикасса/')

    @Property(str, notify=settings_changed)
    def system_id(self):
        if self._system_id:
            return self._system_id

        model = ''
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('model name'):
                    model = line
        from uuid import getnode
        import hmac
        h = hmac.new(b'2017')

        h.update(getnode().to_bytes(8, 'big'))
        h.update(model.encode())
        self._system_id = h.hexdigest()
        logging.warning(self.system_id)
        return self._system_id

    def check(self):
        import hashlib
        import datetime
        now = datetime.datetime.utcnow()
        logging.info(now)
        uid = self.system_id
        s = "{uid}{date:%Y%m%d}{hour}{cl_cons}".format(
            date=now,
            hour=now.hour % 7,
            cl_cons="3456789012",
            uid=self.system_id
            )
        pokey = hashlib.md5(s.encode()).hexdigest()
        url = 'https://kiosk.multidat.ru/api.php?action=CheckLichense&PoKey={key}&uid={uid}'.format(key=pokey,uid=uid)
        resp = {}
        try:
            resp = retry(urllib.error.URLError)(urllib.request.urlopen)(url, timeout=5).read().decode()
            resp = json.loads(resp)
        except urllib.error.URLError:
            exit(403)
        except Exception:
            exit(100)

        if resp.get('err_txt'):
            logging.critical(resp.get('err_txt'))
            exit(int(resp.get('err_no', '403')))
        else:
            #assert self.system_id == resp['uid']
            s = "2109876543{date:%d%m%Y}{hour}{key}".format(
                date=now,
                hour=now.hour % 7,
                key=pokey
            )
            #print(s)
            srvkey = hashlib.md5(s.encode()).hexdigest()
            print(srvkey)
            print(resp)

            if resp['SrvKey'][:-3] != srvkey:
                exit(int(resp.get('err_no', '403')))
            print(resp['SrvKey'][-3:], end="")
            print('ok')
            t = self.checker

            self.checker = Checker(int(resp['SrvKey'][-3:]), self.check)
            self.checker.start()
            return


def exit(code):
    QtCore.QCoreApplication.exit(code)
    sys.exit(code)


def main():

    QtCore.QCoreApplication

    #subprocess.run(['xset', '-dpms'])
    subprocess.run(['xset', 's', 'off', '-dpms'])
    app = QtWidgets.QApplication(sys.argv)
    QtWebEngine.QtWebEngine.initialize()
    engine = QtQml.QQmlApplicationEngine()

    settings = settingsController()
    try:
        settings.check()
        settings.load()
    except:
        subprocess.run(['x-terminal-emulator', '-T', settings.system_id,
                           '-geometry', '146x80', '-e', 'sudo nmtui'])
        exit(403)

    t = threading.Thread(target=settings.while_touch)
    t.daemon = True
    t.start()

    printer = printController(settings.settings, settings)

    ctx = engine.rootContext()
    ctx.setContextProperty('KioskPrinter', printer)
    ctx.setContextProperty('KioskSettings', settings)

    engine.load(QtCore.QUrl("qrc:/Kiosk.qml"))

    c = app.exec_()
    content.resource.qCleanupResources()

    return c


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    exit(main())
