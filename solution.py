#
# Mingyo Random Art
#
# Description: based on mathematical expressions, generate random art, save related text files and image
#, and re-editing images with changing files' names
#
# Author: Mingyo Heo
# Date: oct 19, 2025
#
# input: random mathematical expressions, read expression from text files, resolution, making image counts, make folders' names
# output: image files to png and matematical text files are saved into named folders
#



import random, math, os
from PIL import Image
from math import sin, cos, pi

# Expression generation
from module import png
# Image&text renaming
from module import rename
# Read text file
from module import readText
# Image re-editing 
from module import reEdit
# mplay
from module import mplay



random.seed()

# Evaluate expression string
def evalExpr(expr, x, y):
    try:
        # Define variables and functions
        express = {
            'x': x,
            'y': y,
            'sin': sin,
            'cos': cos,
            'pi': pi,
            'random': random.random,
            'build': {}
        }

        # Use eval function make expression string
        result = eval(expr, express)

        # If result -> complex number => use only real part
        if isinstance(result, complex):
            result = result.real

        # If result -> infinite or no number => 0.0
        if not math.isfinite(result):
            return 0.0

        return result
    
    except:
        return 0.0


# Save expressions to a file path
def writeExprFile(filePath, exprs):
    with open(filePath, "w") as f:

        # Color image
        if isinstance(exprs, dict):
            f.write(f"Color\n")
            f.write(f"R: {exprs['R']}\n")
            f.write(f"G: {exprs['G']}\n")
            f.write(f"B: {exprs['B']}\n")

        # Gray image
        else:
            f.write(f"Gray\n")
            f.write(f"{exprs}\n")

        
# Calculate pixel intensity for Gray
def plotIntensity(expr, pixelsPerUnit = 250, gradX = 0.0, gradY = 0.0,
                  texture = 0.0, weight = 0.1, base = 0.0):
    
    canvasWidth = 2 * pixelsPerUnit
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    for py in range(canvasWidth):
        for px in range(0, canvasWidth):

            # Image size = 2 * pixelsPerUnit (250 -> 500x500)
            # Pixel coordinates
            x = (px - pixelsPerUnit + 0.5) / pixelsPerUnit
            y = (py - pixelsPerUnit - 0.5) / pixelsPerUnit

            # Noise intensity (xpos(left 0) -> right)
            dynamicT = texture * ((x + 1) / 2)
            
            # Control influence
            z = evalExpr(expr, x, y) * weight
            
            # Gradient
            z = z + x * gradX + y * gradY

            # Offset
            z = z + base

            # Before noise
            noiseZ = z

            # Softness
            z = math.tanh(z * 0.8)

            noiseMask = 1.0 - ((noiseZ + 1) / 2)
            dynamicT = texture * noiseMask

            # Random noise
            if dynamicT > 0.001:
                randomNoise = (random.random() * 2 - 1) * dynamicT
                z = z + randomNoise

            # Pixel intensity in the range 0-255
            intensity = int(max(0, min(255, (z + 1) / 2 * 255)))
            canvas.putpixel((px, py), intensity)

    return canvas



# Color setting from plotIntensity
def plotColor(redExpr, greenExpr, blueExpr, pixelsPerUnit = 250):


    redPlane = plotIntensity(redExpr, pixelsPerUnit,
                             gradX = 0.1, gradY = 0.1,
                             texture = 0.5, weight = 0.7,
                             base = 0.7)
    
    greenPlane = plotIntensity(greenExpr, pixelsPerUnit,
                               gradX = 0.2, gradY = 0.3,
                               texture = 0.7, weight = 0.3,
                               base = 0.2)

    bluePlane = plotIntensity(blueExpr, pixelsPerUnit,
                              gradX = 0.1, gradY = 0.2,
                              texture = 0.15, weight = 0.7,
                              base = 0.5)

    return Image.merge("RGB", (redPlane, greenPlane, bluePlane))



# Gray image make and save
def makeGray(numPics = 20, start = 1, imageFolder = "images", textFolder = "text"):
    random.seed()
    
    for i in range(numPics):
        baseName = f"gray.{i}"
        print(f"Gray {i}:")
        grayExp = png.buildExpr()
        print(str(grayExp), "\n")

        
        image = plotIntensity(grayExp, gradY = 1.0, texture = 0.2, weight = 0.8)
              
        image.save(f"{imageFolder}/{baseName}.png", "PNG")
        writeExprFile(f"{textFolder}/{baseName}.txt", grayExp)

        rename.rename(baseName, i, start, imageFolder = imageFolder, textFolder = textFolder)



# Color image make and save
def makeColor(numPics = 20, start = 1, imageFolder = "images", textFolder = "text"):
    random.seed()
    
    for i in range(numPics):
        print(f"Color {i}:")
        redExpr = png.buildExpr()
        print("red =", str(redExpr))
        greenExpr = png.buildExpr()
        print("green =", str(greenExpr))
        blueExpr = png.buildExpr()
        print("blue =", str(blueExpr), "\n")

        exprs = {'R': redExpr, 'G': greenExpr, 'B': blueExpr}
        baseName = f"color.{i}"

        image = plotColor(redExpr, greenExpr, blueExpr)
        image.save(f"{imageFolder}/{baseName}.png", "PNG")
        writeExprFile(f"{textFolder}/{baseName}.txt", exprs)

        rename.rename(baseName, i, start, imageFolder = imageFolder, textFolder = textFolder)



# Count re-edited gray and color images
def countFile(textFolder):

    count = 0
    for filename in os.listdir(textFolder):
        if filename.endswith('.txt'):
            filePath = os.path.join(textFolder, filename)
            try:
                with open(filePath, 'r') as f:
                    firstL = f.readline().strip()
                    if firstL == 'Gray':
                        count += 1
            except Exception:
                continue
    return count



# Ask yes / no to the user (Enter -> default)
def askYesNo(question, default = False):
    hint = "Y/n" if default else "y/N"
    while True:
        try:
            answer = input(f"{question} ({hint}): ").strip().lower()
        except EOFError:
            return default

        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


# Check png images exist in the folder
def hasImages(imageFolder):
    return any(name.endswith(".png") for name in os.listdir(imageFolder))


# Main 
def main():

    # All results go into "RandomArt" folder
    artFolder = "RandomArt"
    imageFolder = os.path.join(artFolder, "images")
    textFolder = os.path.join(artFolder, "text")

    # Number of images to make
    grayNum = 5
    colorNum = 5
    startNum = 1

    # 1. Create RandomArt folder first
    if not os.path.exists(artFolder):
        os.mkdir(artFolder)
        print(f"'{artFolder}' folder created.")

    # 2. Create images and texts folders inside RandomArt
    for folder in (imageFolder, textFolder):
        if not os.path.exists(folder):
            os.mkdir(folder)
            print(f"'{folder}' folder created.")


    # Image generation
    if not hasImages(imageFolder):
        print("No images yet. Make images for the first time.")
        makeNew = True
    else:
        makeNew = askYesNo("Make new images?", default = False)

    if makeNew:
        makeGray(numPics = grayNum, start = startNum, imageFolder = imageFolder, textFolder = textFolder)
        makeColor(numPics = colorNum, start = startNum, imageFolder = imageFolder, textFolder = textFolder)


    # Re-editing (only when images exist)
    if hasImages(imageFolder) and askYesNo("Re-edit images?", default = False):
        level = reEdit.editLevel()

        reEdit.reGray(pixelsPerUnit = 250, imageFolder = imageFolder, textFolder = textFolder, start = 1, level = level)
        reEdit.reColor(pixelsPerUnit = 250, imageFolder = imageFolder, textFolder = textFolder, start = 1, level = level)


    # Images play in mplay
    if hasImages(imageFolder) and askYesNo("Play images in mplay?", default = True):
        mplay.mplay(prefix = "", suffix = ".png", imageFolder = imageFolder)


if __name__ == "__main__":
    main()
