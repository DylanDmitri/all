# Python 2.7 with pyPng
# reads in image, stores it in text files

import png
import os
import shutil

try: shutil.rmtree('uncompressed/')
except OSError: print('making new folder')
os.mkdir('uncompressed/')

f = open('control.txt', 'r')
imagename = next(f).split()[-1].strip()

width, height, image, meta = png.Reader(imagename).asRGBA()

print 'with image - ', imagename
print 'dimensions - ', width, height

redfile = open('uncompressed/red.txt', 'w')
greenfile = open('uncompressed/green.txt', 'w')
bluefile = open('uncompressed/blue.txt', 'w')

colors = (redfile, bluefile, greenfile)

for line in image:

    while line:
        for color in colors:
            color.write(str(line.pop(0))+" ")
        line.pop(0)  # skips transparency level

    for color in colors:
        color.write(';\n')

# note: the output files are semicolon-terminated, non-compliant with numpy standards

print('images read to matrices, run <python3.5 compressor.py> compress the matrices')