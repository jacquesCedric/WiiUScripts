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
        encode(args.file)
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
    sizeToFit = (128,128) if parser.parse_args().icon else (320,120)

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
    new = old.save(imageToConvert.split(".")[0] + ".png")

# Converting to TGA
def convertPNGtoTGA(imageToConvert):
    old = Image.open(imageToConvert)
    resized = resize(old)
    new = resized.save(imageToConvert.split(".")[0] + ".tga")

# Clean up any trailing extensions
def removeExt(stringToEdit):
    return stringToEdit.split(".")[0]


if __name__ == "__main__":
    main()