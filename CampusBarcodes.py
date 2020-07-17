#!/opt/nfv/bin/python3.8
from classes.CampusStudents import Students
from classes.GenerateBarcodes import StringToBarcode
from classes.Pdf import barcodepdf

students = Students()
barcode = StringToBarcode("barcode")
pdfgen = barcodepdf("pdf")


def create_pdf(index, name, id):
    i = index
    if i == 1:
        pdfgen.create_item(name, id, 0, 0)
    if i == 2:
        pdfgen.create_item(name, id, 4, 0)
    if i == 3:
        pdfgen.create_item(name, id, 0, 2)
    if i == 4:
        pdfgen.create_item(name, id, 4, 2)
    if i == 5:
        pdfgen.create_item(name, id, 0, 4)
    if i == 6:
        pdfgen.create_item(name, id, 4, 4)


def main():
    data = students.get_student_ids()
    for person in data:
        barcode.generate(person["ID"], person["ID"])
    i = 1
    for person in data:
        if i < 7:
            create_pdf(i, person["name"], person["ID"])
            i += 1
        else:
            pdfgen.add_page()
            create_pdf(i, person["name"], person["ID"])
            i = 1
    pdfgen.save_pdf("barcodes")
    barcode.clean()


if __name__ == "__main__":
    main()
