#
# Mingyo File Renaming
#
# Description: image and text files are changed to consistency form name
#              Gray image -> BW001, BW002 ...   Color image -> COLOR001, COLOR002 ...
#
# Author: Mingyo Heo
# Date: oct 19, 2025
#
# input: get changable file name, index, start number to get folder path
# output: change names in images folder and text folder
#




import os

grayPrefix = "BW"
colorPrefix = "COLOR"


# Find image type (Gray or Color) from the first line of the text file
def imageType(txtPath):
    with open(txtPath, "r") as f:
        firstLine = f.readline().strip()

    if firstLine == "Color":
        return colorPrefix
    return grayPrefix


# Change name image and text files
def rename(baseName, index, start, prefix = None, imageFolder = "", textFolder = ""):

    baseImage = os.path.join(imageFolder, f"{baseName}.png")
    baseTxt = os.path.join(textFolder, f"{baseName}.txt")

    try:
        # Prefix decided by image type (BW or COLOR)
        if prefix is None:
            prefix = imageType(baseTxt)

        finalName = f"{prefix}{index + start:03d}"
        finalImage = os.path.join(imageFolder, f"{finalName}.png")
        finalTxt = os.path.join(textFolder, f"{finalName}.txt")

        os.rename(baseImage, finalImage)
        os.rename(baseTxt, finalTxt)
        print(f"Files names are changed sucessfully! -> {finalName}")

    except FileNotFoundError:
        print(f"Not Found files in {imageFolder} or {textFolder}")
    except Exception:
        print(f"Error!!")
