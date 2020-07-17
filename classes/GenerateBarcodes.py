#!/opt/nfv/bin/python3.8
import barcode
from barcode import EAN13
from barcode.writer import ImageWriter
import os


class StringToBarcode:
    def __init__(self, name):
        self.name = name

    def generate(self, string, filename):

        file = os.path.join(
            os.path.dirname(__file__), "../barcodes", f"{filename}"
        )
        # or sure, to an actual file:
        ean = barcode.get("Code128", f"{string}", writer=ImageWriter())
        filename = ean.save(file, options={"write_text": False})
        return filename
