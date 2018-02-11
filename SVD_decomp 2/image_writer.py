# Python 2.7 with pyPng
# builds compressed image for each file

import png
import os
import shutil

try: shutil.rmtree('compressed_images/')
except OSError: print('making new folder')
os.mkdir('compressed_images/')

f = open('control.txt', 'r')
imagename = next(f).split()[-1].strip()
terms = tuple(next(f).split(':')[-1].strip().split(', '))

def rowgen():

    red = open(rfolder + 'red.txt', 'r')
    blue = open(rfolder + 'blue.txt','r')
    green = open(rfolder + 'green.txt','r')

    for rows in zip(red, blue, green):
        r = []
        for trip in zip(*(map(int, row.split()) for row in rows)):
            r.extend(trip)
        yield r


wfolder = 'compressed_images/{}terms__{}_percent_filesize.png'
for t in terms:
    rfolder = 'compressed_matrices/' + str(t) + '/'

    info = open(rfolder + 'info', 'r').read()
    width, height = info.split('\n')[0].split()[2].split('x')
    t, width, height = int(t), int(width), int(height)

    percent = 100 * (t + t * (width + height)) / (width * height)

    png.Writer(width=width, height=height, alpha=False).write(
        open( wfolder.format(t, percent), 'w'),
        rowgen()
    )

print('all images compressed to pngs. Enjoy!')




