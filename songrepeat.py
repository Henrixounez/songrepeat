#!/usr/bin/python3

import sys
import numpy as np
from PIL import Image as Img

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

def createImagePixels(contentLength, array):
  img_array = np.zeros((contentLength, contentLength, 3), dtype=np.uint8)
  for i in range(contentLength):
    for u in range(contentLength):
      if array[i][u] > 0:
        img_array[i][u] = [255, 255, 255]
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
  content = getFileContents()
  contentLength = len(content)
  array = createArray(content, contentLength)
  img = Img.fromarray(createImagePixels(contentLength, array), 'RGB')
  imageRender(contentLength, img)