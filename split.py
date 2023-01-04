#!/usr/bin/env python3
from pdfrw import PdfReader, PdfWriter, PageMerge


def pdf_input():
	file = input('Please write the name of the PDF you want to split.\nRemember that the PDF must be in the same folder as this program')
	if file and not file.lower().endswith('.pdf'): #in case they don't write .pdf or write it in uppercase
		return file + '.pdf'
	return file

def splitpage(file, place):
	page = PageMerge()

	for x_pos in (0,0.5):
		page.add(file, viewrect=(x_pos, 0, place,1))
		yield page.render()

def write_new_pdf(file):
	writer = PdfWriter()

	try:
		pages = PdfReader(file).pages #No es CaseSensitive :)
	except:
		return

	for page in pages:
		writer.addpages(splitpage(page))

	with open(f"new_{file}","wb") as nuevo:
		writer.write(nuevo)

def main():
	file = pdf_input()
	print(file)
	if not file: return
	write_new_pdf(file)


