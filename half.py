import pdf2image
import numpy as np
import os
import binary
import split
from pdfrw import PdfReader, PdfWriter, PageMerge

def splitpage(file, place):
	page = PageMerge()
	for x_pos in (0,0.5):
		page.add(file, viewrect=(x_pos, 0, place,1))
		yield page.render()

def main(): #BINARY FUNCIONA, ESTO NO

    pages = pdf2image.convert_from_path("pasajes.pdf", 500)
    print(len(pages))
    writer = PdfWriter()


    for page in pages:
        name = "page.png"
        page.save(os.path.join(name), 'PNG')

        center = binary.center_of_texts("page.png")
        print(center)
        #left,right = binary.crop_image('page.png', center)
        print(page.width)
        ratio = center[1]/page.width
        print(ratio)
        writer.addpages(splitpage(page,ratio))

        #writer.addpage(left)
        #writer.addpage(right)

    with open(f"new","wb") as nuevo:
        writer.write(nuevo)


main()