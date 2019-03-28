'''

def template1(ti):
    TPL1 = "{film}"

    TPL2 = "{data}  {time}"

    TPL3 = """
    {zal}
    {seat}




     {price}
     {kassa}
    """

    w=482
    h=722
    font_size=32

    img = Image.new('RGBA', (h, w), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font3 = ImageFont.truetype("DejaVuSans.ttf", 28)
    font2 = ImageFont.truetype("DejaVuSans.ttf", 24)

    draw.multiline_text((0,25), TPL1.format(**ti), font=font3, fill=(0,0,0))
    draw.multiline_text((22,95), TPL2.format(**ti), font=font2, fill=(0,0,0))
    draw.multiline_text((22,95), TPL3.format(**ti), font=font3, fill=(0,0,0), spacing=2)
    # img.show()
    imgr = img.rotate(-90,expand=1)
    return imgr



from PySide2.QtSvg import QSvgRenderer
from PySide2.QtGui import QImage, QPainter
from PySide2.QtCore import QBuffer, QByteArray, QIODevice




def template2(ti):
    
data = ""
with open('../forms/kinobilet.svg', 'r') as fsvg:
    data = fsvg.read()
   
   
data = data.format(**ti).encode()
qsvg = QSvgRenderer(QByteArray(data))
iq = QImage(w, h, QImage.Format_ARGB32)
p = QPainter(iq)
qsvg.render(p)

buf = QBuffer()
buf.open(QIODevice.ReadWrite)
iq.save(buf, 'png')
img = Image.frombytes('RGBA', (w, h), buf.data())
imgr = img.rotate(-90,expand=1)
return imgr

import pdb

pdb.run('template2(ti)')


        #imgr = img.rotate(-90, expand=1)
        #imgr.show()

'''

ti={'film': 'Тестовое кино', 'zal': 'Зал 4', 'seat': 'Ряд 1, место 1', 'time': '20:00', 'data': '26.02.2019', 'price': 280, 'kassa': 'Онлайн касса'}

w=482
h=722

import datetime
import cairosvg
from io import BytesIO
from PIL import Image
from util import retry
import urllib.request

class Template:
    
    def __init__(self, template, *a, **kw):
        self.file = template
        self.tpl = None
    
    @property
    @retry(urllib.error.URLError)
    def template(self):
        if self.tpl:
            return self.tpl
        if self.file.startswith('http'):
            self.tpl = urllib.request.urlopen(self.file).read().decode()
        else:
            with open(self.file, 'r') as fsvg:
                self.tpl = fsvg.read()
        return self.tpl

    def render(self, ticket):
        now = datetime.datetime.now()
        tpl = self.template.format(now=now, **ticket)
        buff = BytesIO()
        cairosvg.svg2png(dpi=204, bytestring=tpl, write_to=buff)
        buff.seek(0)
        img = Image.open(buff)
        return img
    

#imgr = Template('../forms/bilet-90.svg').fill(ti)


