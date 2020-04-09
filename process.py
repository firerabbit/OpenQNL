#!/usr/bin/env python

from PIL import Image
from optparse import OptionParser
import os

# Run this first on a video file to generate a sequence of images
# ffmpeg -i aerial.mp4 -vf fps=4 out%d.png

parser = OptionParser()
parser.add_option("-i", "--input", dest="filename")
parser.add_option("-o", "--output", dest="output")
parser.add_option("-n", "--num", dest="num")
parser.add_option("-y", "--height", dest="height")

options, args = parser.parse_args()
filename = options.filename or 'out%d.png'
output = options.output or 'output.png'
num = int(options.num or 100)
y = int(options.height or 50)

print filename

first_filename = filename % 1
print 'first file=%s' % first_filename
i = Image.open(first_filename)
w, h = i.size
i.close()

om = Image.new('RGB', (w, y * num))

for i in xrange(1, num+1):
  # Crop a 2 pixel sliver
  im = Image.open(filename % i)
  # Sliver in the middle of the image
  top = h / 2 # h - y
  crop_box = (0, top, w, top + y)
  paste_box = (0, (i-1)*y, w, (i)*y)
  print "copying from %s to %s" % (crop_box, paste_box)
  r = im.crop(crop_box)
  om.paste(r.rotate(180), paste_box)

om.save(output)
print 'wrote %s' % output
