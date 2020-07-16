#!/opt/nfv/bin/python3.8
from fpdf import FPDF

pdf = FPDF(orientation="P", unit="in", format="Letter")
pdf.add_page()
pdf.set_font("Arial", size=15)


class barcodepdf:
    def __init__(self, name):
        self.name = name

    def create_item(self, personname, barcode, x_offset, y_offset):
        pdf.rect(x=0.4 + x_offset, y=0.4 + y_offset, w=4, h=2, style="D")
        pdf.text(x=2 + x_offset, y=1 + y_offset, txt=f"{personname}")
        pdf.image(
            f"./barcodes/{barcode}.png",
            w=3,
            h=1,
            x=0.75 + x_offset,
            y=1.25 + y_offset,
        )

    def save_pdf(self, filename):
        pdf.output(f"./pdfs/{filename}.pdf")

    def add_page(self):
        pdf.add_page()
