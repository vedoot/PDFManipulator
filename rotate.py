import sys
import os

from pdfrw import PdfReader, PdfWriter

inpfn = sys.argv[1]

outfn = 'rotate.%s' % os.path.basename(inpfn)
trailer = PdfReader(inpfn)
pages = trailer.pages
for i in range(0, len(pages), 2):
    pages[i].Rotate  = 180
print("I luv u")
outdata = PdfWriter(outfn)
outdata.trailer = trailer
outdata.write()
