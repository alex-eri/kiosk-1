import printer
import template
from PySide2.QtCore import QCoreApplication, QObject, Signal, Slot, Property
import sys
import subprocess
import shlex
import json
import urllib.request
import time
import logging
import smtplib
from email.message import EmailMessage
import datetime


def exit(code):
    QCoreApplication.exit(code)
    sys.exit(code)

class printController(QObject):
    def __init__(self, settings, sc):
        QObject.__init__(self)

        self.settings = settings
        self.sc = sc
        self._tickets = []
        self._error = ''
        self._printer = None
        self._template = None
        self._number = 0
        self._tcount = sc.local_settings.get('counters',{}).get('loaded',0)
        self._pcount = sc.local_settings.get('counters',{}).get('printed',0)
        self.on_counter.emit()

    @property
    def printer(self):
        if not self._printer:
            if self.settings.get('printer'):
                self._printer = printer.Printer(**self.settings.get('printer'))
        return self._printer

    @property
    def template(self):
        if not self._template:
            if self.settings.get('printer'):
                self._template = template.Template(**self.settings.get('printer'))
        return self._template

    @Slot(int)
    def feed_and_cut(self, count):
        self.tcount = int(count) - 1
        self.printer.printer.text("Last: %d \n" % self.pcount)
        self.printer.printer.text("Load: %d \n" % count)
        self.printer.printer.text("Avail: %d \n" % (self.tcount-1))
        self.printer.printer.text("###\n"*9)
        self.printer.cut()
        self._pcount = 1

    @Slot(str, 'QJSValue')
    def get(self, text, success):
        self.number = 0
        text = text.strip()
        print(text)
        if text == "#66884":
            subprocess.run(['x-terminal-emulator', '-T', 'Network Settings',
                           '-geometry', '146x80', '-e', 'sudo nmtui'])
            return
        elif text == "#66174":
            subprocess.run(['x-terminal-emulator'])
            return
        elif text == "#66170":
            #self.error = self.settings
            return
        elif text.startswith("#075#"):
            self.feed_and_cut(int(text.split('#')[-1]))
            return
        elif text == "#85789":
            exit(0)
            return
        elif text == "#07564":
            pass
        elif "#" in text:
            self.error = "нет"
            return

        url = self.settings['api']['url'] + 'getBilet?key=' + self.settings['api']['key'] + '&bilet=' + text
        try:
            r = urllib.request.urlopen(url)
        except urllib.error.URLError:
            self.error = "Сервис не доступен"
            return

        if r.status != 200:
            self.error = "Ошибка сети: %d %s" % (r.code, r.reason)
            return

        resp = json.loads(r.read().decode())

        if 'tickets' in resp:
            self._tickets = resp.get('tickets', [])
            self.number = text
            self.on_tickets.emit()
            success.call()
            #print(self.tickets)


        if 'error' in resp:
            self.error = "%s" % resp.get('description')


    on_error = Signal()
    on_tickets = Signal()
    on_number = Signal()

    @Property(str, notify=on_number)
    def number(self):
        return self._number

    @number.setter
    def set_number(self, v):
        if self._number != v:
            self._number = v
            self.on_number.emit()

    on_counter = Signal()

    @Property(int, notify=on_counter)
    def tcount(self):
        print('...')
        return self._tcount

    @tcount.setter
    def set_tcount(self, v):
        self._tcount = v
        self.save_counters()

    @Property(int, notify=on_counter)
    def pcount(self):
        print('...')
        return self._pcount

    @pcount.setter
    def set_pcount(self, v):
        self._pcount = v
        self.save_counters()

    def save_counters(self):
        self.sc.local_settings['counters'] = {
            "loaded": self.tcount,
            "printed": self.pcount
        }

        self.sc.save_local_settings()
        self.on_counter.emit()
        try:
            self.email()
        except Exception:
            logging.error('cant send email')

    def email(self):
        if self.settings.get('notify') and self.settings.get('notify').get('to'):
            msg = EmailMessage()
            msg['Subject'] = '%d бланков в терминале' % self.tcount
            msg['From'] = 'kiosk@eri.su'
            msg['To'] = self.settings['notify']['to']
            msg.set_content("{now:%d.%m.%Y %H:%M}."
                            " В терминале «{system_id}»"
                            " на катушке осталось {count} количество бланков.".format(
                                count=self.tcount,
                                system_id=self.sc.system_id,
                                now=datetime.datetime.now()
                            )

                            )
            with smtplib.SMTP(host="smtp.elasticemail.com", port=2525) as s:
                s.login("alexander.eerie@gmail.com", "188d079d-3be4-497f-8c0c-9a913480b1df")
                s.send_message(msg)

    @Property(str, notify=on_error)
    def error(self):
        return self._error

    @error.setter
    def set_error(self, v):
        if self._error != v:
            self._error = v
            self.on_error.emit()

    @Property('QVariantList', notify=on_tickets)
    def tickets(self):
        return self._tickets

    @Slot('QJSValue')
    def print(self, success):
        if len(self._tickets) >= self.tcount:
            self.error = "Не хватит бумаги"

        while self._tickets:
            try:
                if self.printer.printer.paper_status() == 0:
                    self.error = "Нет бумаги"
                    return
            except NotImplementedError:
                pass
            except Exception:
                self.error = "Ошибка печати"

            t = self._tickets.pop()
            img = self.template.render(t)

            try:
                self._tcount -= 1
                self.printer.print(img)
            except Exception:
                self.error = "Ошибка печати"
            self._pcount += 1
            self.on_tickets.emit()
            time.sleep(self.settings['printer'].get('delay', 1))
            self.printer.cut()

        self.save_counters()


        if self.submit():
            success.call()

        #error.call()


    def submit(self):
        "api/setPrintStatus?key=876543210&bilet=789464&status=ok"
        if self.number and self.settings['api'].get('commit'):
            url = self.settings['api']['url'] + 'setPrintStatus?key=' + self.settings['api']['key'] + '&bilet=' + self.number + '&status=ok'
            print(url)
            try:
                r = urllib.request.urlopen(url)
            except urllib.error.URLError:
                self.error = "Сервис не доступен"
                return False
        return True
