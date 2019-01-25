import os
import argparse

from pdfrw import PdfReader, PdfWriter, PageMerge


def fixpage(*pages):
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()


parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input pdf file name")
parser.add_argument("-p", "--padding", action = "store_true",
                    help="Padding the document so that all pages use the same type of sheet")
args = parser.parse_args()

inpfn = args.input
outfn = 'booklet.' + os.path.basename(inpfn)
ipages = PdfReader(inpfn).pages

if args.padding:
    pad_to = 4
else:
    pad_to = 2

# Make sure we have a correct number of sides
ipages += [None]*(-len(ipages)%pad_to)

opages = []
while len(ipages) > 2:
    opages.append(fixpage(ipages.pop(), ipages.pop(0)))
    opages.append(fixpage(ipages.pop(0), ipages.pop()))

opages += ipages

PdfWriter(outfn).addpages(opages).write()





# import sys
# import os
#
# from pdfrw import PdfReader, PdfWriter, PageMerge
#
#
# def get4(srcpages):
#     scale = 0.5
#     srcpages = PageMerge() + srcpages
#     x_increment, y_increment = (scale * i for i in srcpages.xobj_box[2:])
#     for i, page in enumerate(srcpages):
#         page.scale(scale)
#         page.x = x_increment if i & 1 else 0
#         page.y = 0 if i & 2 else y_increment
#     return srcpages.render()
#
#
# inpfn, = sys.argv[1:]
# outfn = '4up.' + os.path.basename(inpfn)
# pages = PdfReader(inpfn).pages
# writer = PdfWriter(outfn)
# for index in range(0, len(pages), 4):
#     writer.addpage(get4(pages[index:index + 4]))
# writer.write()




# import os
#
# from pdfrw import PdfReader, PdfWriter
#
# inpfn = sys.argv[1]
#
# outfn = 'rotate.%s' % os.path.basename(inpfn)
# trailer = PdfReader(inpfn)
# pages = trailer.pages
# for i in range(0, len(pages), 2):
#     pages[i].Rotate  = 180
# outdata = PdfWriter(outfn)
# outdata.trailer = trailer
# outdata.write()
