import pyqrcode

qr = pyqrcode.create('happy monday')
qr.png('abc.png')