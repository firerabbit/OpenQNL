#!/usr/bin/env python

from PIL import Image
from optparse import OptionParser
import os

# Run this first on a video file to generate a sequence of images
# ffmpeg -i aerial.mp4 -filter:v "crop=3840,50,0,1055" -vf fps=16 tmp/out%d.png

# Usage: converts a sequence of 222 files named out1.png - out222.png
# with sliver heights of 14 pixels per image into output.png
# ./process.py -i 'out%d.png' -n 222 -y 14 -o 'output.png'

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

try:
    for i in xrange(1, num+1):
      # Crop a 2 pixel sliver
      im = Image.open(filename % i)
      # Sliver in the middle of the image
      top = h / 2 # h - y
      crop_box = (0, top, w, top + y)
      paste_box = (0, (i-1)*y, w, (i)*y)
      print "i=%s copying from %s to %s" % (i, crop_box, paste_box)
      r = im.crop(crop_box)
      om.paste(r.rotate(180), paste_box)
except Exception, err:
    print err
finally:
  om.save(output)
  print 'wrote %s' % output
