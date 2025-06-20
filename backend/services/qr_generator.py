import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer
import qrcode.constants
import hashlib


class Qrcode:
    def __init__(self):
        self.data = None
        # задание параметров QR
        self.qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        self.qr_img = None

    def add_data(self, data):
        self.data = Qrcode._data_to_hash(data)
        self.qr.clear()
        self.qr.add_data(self.data)

    # создаем изображение 
    def make_qr(self):
        self.qr_img = self.qr.make_image(image_factory=StyledPilImage, module_drawer=CircleModuleDrawer())


    @staticmethod
    def _data_to_hash(data) -> str: 
        return str(hashlib.sha256(str(data).encode('utf-8')).hexdigest())

qr = Qrcode()
qr.add_data('Misha.com')
qr.make_qr()
qr.qr_img.show()
    