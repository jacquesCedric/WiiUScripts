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
   Fetch idbe images from Nintendo and decode them into usable format.
   Requires Python3 and should be platform agnostic.
   
   This scripts would not have been possible without the work by NexoCube, NWPlayers123, and whomever 
   created this entry - http://wiiubrew.org/wiki/Nn_idbe.rpl
   NexoCube and NWPlayers123 projects can be found at:
   - https://gist.github.com/NWPlayer123/7e6233aee364796c55d85f143bba4bd1
   - https://github.com/NexoDevelopment/idbe_decrypt/blob/master/idbe_decrypt.py
"""

import sys, io
import requests, urllib3
import argparse
# Note: Crypto may give you some issues. Use pip3 to uninstall Crypto and Pycrypto, then reinstall package "pycrypto"
from Crypto.Cipher import AES
from struct import unpack
import re
import os

urllib3.disable_warnings()

idbe_url = "https://idbe-wup.cdn.nintendo.net/icondata/10/"

IV = "A46987AE47D82BB4FA8ABC0450285FA4" # Init Vector (for AES-128-CBC)

# Keys used to decrypt the idbe content
K0 = "4AB9A40E146975A84BB1B4F3ECEFC47B" # aes_keys[0]
K1 = "90A0BB1E0E864AE87D13A6A03D28C9B8" # aes_keys[1]
K2 = "FFBB57C14E98EC6975B384FCF40786B5" # aes_keys[2]
K3 = "80923799B41F36A6A75FB8B48C95F66F" # aes_keys[3]

AES_KEYS = [K0, K1, K2, K3]


# Argument if run as script
parser = argparse.ArgumentParser(description="Fetch idbe images from Nintendo and decode them into usable format.")
parser.add_argument("titleID", metavar="titleID", type=str,
                    help="the titleID of the icon you want", nargs="?", const="")

def main():
    args = parser.parse_args()

    if (args.titleID):
        print("Attempting retrieval and decode of image")
        fetchIcon(args.titleID)
        print("Through the gauntlet")
    else:
        with open('titleIDs', 'r') as f:
            for line in f:
                t = line[:16]
                fetchIcon(t)

# Called externally, if used as module
# returns the name of the icon file and the titleID
def fetchIcon(titleID):
    titleID = sanitize(titleID)
    fetchIDBE(titleID)
    return decodeIDBE(titleID)
    
# Clean up title_id strings
def sanitize(arg):
    arg = arg.upper()
    arg = re.sub('[^0-9a-zA-Z]+', '', arg)
    if len(arg) != 16:
        print("Title format not correct")
        sys.exit()
    return arg

# Download the correct IDBE file
def fetchIDBE(titleID):
    fileName = titleID + ".idbe"
    url = idbe_url + fileName

    # Download the .idbe file from Nintendo
    r = requests.get(url, stream=True, verify=False)
    with open(fileName, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
        f.close()
    

# returns the name of the icon file and the titleID    
def decodeIDBE(titleID):
    directory = "icons/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)

    fileName = directory + titleID + ".tga"

    # Get what we need from the idbe file
    with open(titleID + ".idbe", "rb") as f:
        first = f.read(1)
        first = ord(first)

        # Check the header is correct
        try:
            assert(first == 0)
            print("grabbing icon for: " + titleID)
            # Which AES key do we need to decrypt
            key = ord(f.read(1))

            # Magic type-casting
            AES_KEY = bytes(bytearray.fromhex(AES_KEYS[key]))
            IV_KEY = bytes(bytearray.fromhex(IV))

            # Let's decrypt
            aes = AES.new(AES_KEY, AES.MODE_CBC, IV_KEY)
            idbe = aes.decrypt(f.read())

            # Grab the title
            title = idbe[0x250:0x250+0x80]
            title = title.decode("UTF-16-BE")

            # write our tga file
            with open(fileName, "wb") as newFile:
                newFile.write(idbe[0x2050:])
                os.remove(titleID + ".idbe")

                # if everything works we return these two
                return fileName, title
        except:
            print("failed for: " + titleID)
            return


# if standalone script
if __name__ == "__main__":
    main()
