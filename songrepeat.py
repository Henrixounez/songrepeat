#!/usr/bin/python3

import sys
import numpy as np
from PIL import Image as Img
from binascii import crc32

## ColorHash from https://pypi.org/project/colorhash/
def hsl2rgb(h, s, l):
  h /= 360
  q = l * (1 + s) if l < 0.5 else l + s - l * s
  p = 2 * l - q
  rgb = []
  for c in (h + 1 / 3, h, h - 1 / 3):
    if c < 0:
      c += 1
    elif c > 1:
      c -= 1
    if c < 1 / 6:
      c = p + (q - p) * 6 * c
    elif c < 0.5:
      c = q
    elif c < 2 / 3:
      c = p + (q - p) * 6 * (2 / 3 - c)
    else:
      c = p
    rgb.append(round(c * 255))
  return tuple(rgb)

def colorHash(s):
  saturation=(0.35, 0.5, 0.65)
  hash = crc32(s.encode('utf-8')) & 0xffffffff
  h = (hash % 359)
  hash //= 360
  s = saturation[hash % len(saturation)]
  hash //= len(saturation)
  l = 0.7
  return hsl2rgb(h, s, l)

####

def createArray(content, contentLength):
  array = []
  for i in range(contentLength):
    array.append([])
    for u in range(contentLength):
      if content[i] == content[u]:
        if i > 0 and u > 0 and i != u and array[i - 1][u - 1] != 0:
          array[i].append(array[i - 1][u - 1] + 1)
        else:
          array[i].append(1)
      else:
        array[i].append(0)
  return array

def checkArgs():
  if len(sys.argv) < 2:
    print('Please give a text file as an argument')
    sys.exit(1)
  if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print('./songrepeat.py file [-s]')
    print('-h , --help : Show this help')
    print('-s , --save : Saves the output image')
  file = sys.argv[1]
  return file

def getFileContents():
  try:
    fd = open(file, "r")
  except:
    print('File doesn\'t exists')
    sys.exit(1)
  content = fd.read()
  content = content.split()
  return content

def createImagePixels(content, contentLength, array):
  img_array = np.zeros((contentLength, contentLength, 3), dtype=np.uint8)
  for i in range(contentLength):
    for u in range(contentLength):
      if array[i][u] > 0:
        img_array[i][u] = colorHash(content[i])
  return img_array

def imageRender(contentLength, img):
  if len(sys.argv) > 2 and (sys.argv[2] == '-s' or sys.argv[2] == '--save'):
    img2 = img.resize((contentLength * 5, contentLength * 5), Img.NEAREST)
    img2.save(file.split('/')[-1] + "_songrepeat.png", "png")
  else:
    img2 = img.resize((900, 900), Img.NEAREST)
    img2.show()

if __name__ == "__main__":
  file = checkArgs()
  try:
    content = getFileContents()
  except:
    print('File is not text')
    sys.exit(1)
  contentLength = len(content)
  array = createArray(content, contentLength)
  img = Img.fromarray(createImagePixels(content, contentLength, array), 'RGB')
  imageRender(contentLength, img)