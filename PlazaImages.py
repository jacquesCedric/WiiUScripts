import sys, io
import argparse
import zlib
import base64
from PIL import Image

# Should
parser = argparse.ArgumentParser(description="Convert an image to a base64, zlib-compressed string - for use in Wara Wara Plaza.")
parser.add_argument("file", metavar="File", type=str,
                    help="the image or file to be processed")
parser.add_argument("-d", "--decode", action="store_true",
                    help="decode a string from Wara Wara Plaza into a .png image")


def main():
    args = parser.parse_args()

    if args.decode:
        print("Attempting decoding of image")
        decode(args.file)
        print("Through the gauntlet")
    else:
        print("Attempting encode of image")
        encode(args.file)
        print("Through the gauntlet")


def decode(stringToDecode):
    with open(stringToDecode) as file:
        decode = base64.b64decode(file.read())
        image = zlib.decompress(decode)

        newName = removeExt(stringToDecode) + ".tga"

        with open(newName, "wb") as newImage:
            newImage.write(image)
            newImage.close()

        convertTGAtoPNG(newName)


def encode(imageToEncode):
    if imageToEncode[-4:] != ".tga":
        convertPNGtoTGA(imageToEncode)

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
def resize(imageToResize):
    print("resizing not implemented")

def convertTGAtoPNG(imageToConvert):
    old = Image.open(imageToConvert)
    new = old.save(imageToConvert.split(".")[0] + ".png")

def convertPNGtoTGA(imageToConvert):
    old = Image.open(imageToConvert)
    new = old.save(imageToConvert.split(".")[0] + ".tga")

# Clean up any trailing extensions
def removeExt(stringToEdit):
    return stringToEdit.split(".")[0]


if __name__ == "__main__":
    main()