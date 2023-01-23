import pdf2image
import os
import binary
from pdfrw import PdfReader, PdfWriter, PageMerge

def splitpage(file, place):
	page = PageMerge()
	for x_pos in (0,place):
		page.add(file, viewrect=(x_pos, 0, place,1))
		yield page.render()

def main(): #BINARY FUNCIONA, ESTO NO
    cwd = os.getcwd()
    pages = pdf2image.convert_from_path("vegas.pdf", 500)
    print(len(pages))
    # 1 min para 37 paginas
    file = "vegas.pdf"
    writer = PdfWriter()
    pages_reader = PdfReader(file).pages
    index = 0
    for page in pages:
        print("page: ",index)
        name = "page.png"
        page.save(os.path.join(name), 'PNG')
        center = binary.center_of_texts("page.png")
        print("center: ",center)
        #left,right = binary.crop_image('page.png', center)
        ratio = center[0]/page.width
        print("width: ",page.width)
        print("ratio: ",ratio)
        #if ratio > 0.75 or ratio < 0.25:
        #    print("strange ratio")
        #    ratio = 0.5

        writer.addpages(splitpage(pages_reader[index],ratio))
        index += 1
        print()
        #writer.addpage(left)
        #writer.addpage(right)

    with open(f"new.pdf","wb") as nuevo:
        writer.write(nuevo)


main()