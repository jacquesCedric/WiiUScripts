#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Jacob Gold"
__copyright__ = "Copyright 2007, Jacob Gold"
__credits__ = ["Jacob Gold"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jacob Gold"
__status__ = "Prototype"

"""
   Translating images to and from Nintendos Base64, zlib-compressed format.
"""

import sys, io
import argparse
import zlib
import base64
from PIL import Image

parser = argparse.ArgumentParser(description="Convert an image to a base64, zlib-compressed string - for use in Wara Wara Plaza.")
parser.add_argument("file", metavar="File", type=str,
                    help="the image or file to be processed")
parser.add_argument("-d", "--decode", action="store_true",
                    help="decode a string from Wara Wara Plaza into a .png image")
parser.add_argument("-i", "--icon", action="store_true",
                    help="Set desired output dimensions to that of an icon(128x128), default dimensions are of painting size(320x120)")

def main():
    args = parser.parse_args()

    if args.decode:
        print("Attempting decoding of image")
        decode(args.file)
        print("Through the gauntlet")
    else:
        print("Attempting encode of image")
        encode(args.file, args.icon)
        print("Through the gauntlet")

# Convert image to tga, zlib compress, then base64encode
# Output is [FileName].data
def decode(stringToDecode):
    with open(stringToDecode) as file:
        decode = base64.b64decode(file.read())
        image = zlib.decompress(decode)

        newName = removeExt(stringToDecode) + ".tga"

        with open(newName, "wb") as newImage:
            newImage.write(image)
            newImage.close()

        convertTGAtoPNG(newName)

# Take data string, base64decode, decompress result, convert to png
# Output is TGA and PNG images from data
def encode(imageToEncode, isIcon = False):
    if imageToEncode[-4:] != ".tga":
        convertIMGtoTGA(imageToEncode, isIcon)

    imageToEncode = removeExt(imageToEncode) + ".tga"

    with open(imageToEncode, "rb") as image:
        byteImage = bytearray(image.read())
        compress = zlib.compress(byteImage)
        encode = base64.b64encode(compress)

        newName = removeExt(imageToEncode) + ".data"

        with open(newName, "wb") as newFile:
            newFile.write(encode)
            newFile.close()    

# We may want to resize an image if this script is fed something that's the wrong size
def resize(imageToResize, isIcon):
    sizeToFit = (128,128) if isIcon else (320,120)

    # Find ratios
    widthRatio = float(sizeToFit[0]) / float(imageToResize.size[0])
    heightRatio = float(sizeToFit[1]) / float(imageToResize.size[1])

    # Find potential new values
    potentialWidth = float(imageToResize.size[0]) * heightRatio
    potentialHeight = float(imageToResize.size[1]) * widthRatio

    if (potentialWidth < sizeToFit[0]):
        newSize = sizeToFit[0], int(potentialHeight)
    else:
        newSize = int(potentialWidth), sizeToFit[1]

    imageToResize = imageToResize.resize(newSize, Image.ANTIALIAS)

    # crop
    imageToResize = imageToResize.crop((0, 0, sizeToFit[0], sizeToFit[1]))

    #return image
    return imageToResize


# Converting to PNG
def convertTGAtoPNG(imageToConvert):
    old = Image.open(imageToConvert)
    new = old.save(removeExt(imageToConvert) + ".png")

# Converting to TGA
def convertIMGtoTGA(imageToConvert, isIcon):
    old = Image.open(imageToConvert)
    resized = resize(old, isIcon)
    if resized.mode == "RGB":
        alph = Image.new('L', resized.size, 255)
        resized.putalpha(alph)
    new = resized.save(removeExt(imageToConvert) + ".tga")

# Clean up any trailing extensions
def removeExt(stringToEdit):
    return stringToEdit.split(".")[0]


if __name__ == "__main__":
    main()