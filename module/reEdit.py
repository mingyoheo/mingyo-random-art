#
# Mingyo Image Re-editing
#
# Description: From text files, put randering parameter and re-plot Gray and Color images. Users put re-editing level. 
#
# Author: Mingyo Heo
# Date: oct 19, 2025
#
# input: re-editing images and text files from folders, pixerls per unit, start number and recursive level
# output: save re-editing new images and rename the files
#



import os
import random
import math
from PIL import Image
from math import sin, cos, pi
from . import png
from . import readText
from . import rename


# Same expression evaluation function with solution.py
def evalExpr(expr, x, y):
    try:
        express = {
            'x': x,
            'y': y,
            'sin': sin,
            'cos': cos,
            'pi': pi,
            'random': random.random,
            'build': {}
        }

        result = eval(expr, express)

        if isinstance(result, complex):
            result = result.real

        if not math.isfinite(result):
            return 0.0

        return result
    
    except:
        return 0.0


# Gray image re-editing
def reGray(expr = None, pixelsPerUnit = 250, gradX = 0.0, gradY = 0.1,
                  texture = 0.3, weight = 3.0, base = 0.0, imageFolder = "images", textFolder = "text", start = 1, level = 8):

    # Read only gray image text file
    if expr is None:
        import os
        global readText

        for filename in sorted(os.listdir(textFolder)):
            if filename.endswith('.txt'):
                filePath = os.path.join(textFolder, filename)
                try:
                    exprData = readText.readFile(filePath)

                    if isinstance(exprData, str):
                        print(f"Process in recreating gray image")

                        image = reGray(exprData, pixelsPerUnit, gradX, gradY, texture, weight, base,
                                       imageFolder, textFolder, start, level)

                        # BW001 -> ReBW001 (original image is kept)
                        baseName = os.path.splitext(filename)[0]
                        reName = f"Re{baseName}"
                        finalPath = os.path.join(imageFolder, f"{reName}.png")
                        image.save(finalPath, "PNG")
                        print(f"Saved recreated gray image {reName}")

                    elif isinstance(exprData, dict):
                        print(f"Skip color file")
                        continue

                except Exception:
                    print(f"Error processing {filename}")
        return None
    
    canvasWidth = 2 * pixelsPerUnit
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    for py in range(canvasWidth):
        for px in range(0, canvasWidth):
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
            z = math.cos(z * 4)

            noiseMask = 1.0 - ((noiseZ + 1) / 2)
            dynamicT = texture * noiseMask

            # Random noise
            if dynamicT > 0.001:
                randomNoise = (random.random() * 2 - 1) * dynamicT
                z = z + randomNoise

            intensity = int(max(0, min(255, (z + 1) / 2 * 255)))
            canvas.putpixel((px, py), intensity)

    return canvas

    
# Color image replotting logic (same with reGray)
def rePlot(expr, pixelsPerUnit = 250, gradX = 0.0, gradY = 0.15, texture = 0.3, weight = 1.0, base = 0.0):
    
    canvasWidth = 2 * pixelsPerUnit
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    for py in range(canvasWidth):
        for px in range(0, canvasWidth):
            x = (px - pixelsPerUnit + 0.5) / pixelsPerUnit
            y = (py - pixelsPerUnit + 0.5) / pixelsPerUnit

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
            z = math.cos(z * 4)

            noiseMask = 1.0 - ((noiseZ + 1) / 2)
            dynamicT = texture * noiseMask

            # Random noise
            if dynamicT > 0.001:
                randomNoise = (random.random() * 2 - 1) * dynamicT
                z = z + randomNoise

            intensity = int(max(0, min(255, (z + 1) / 2 * 255)))
            canvas.putpixel((px, py), intensity)

    return canvas
    

# R,G,B channels for color image replotting
def reColorEdit(redExpr, greenExpr, blueExpr, pixelsPerUnit = 250, level = 8):

    def randomGrad():
         return random.uniform(0.0, 0.5)
    
    redPlane = rePlot(redExpr, pixelsPerUnit, gradX = randomGrad(), gradY = randomGrad(), texture = 0.0,
                      weight = 1.0, base = randomGrad())
    greenPlane = rePlot(greenExpr, pixelsPerUnit, gradX = randomGrad(), gradY = randomGrad(), texture = 0.0,
                      weight = 1.0, base = randomGrad())
    bluePlane = rePlot(blueExpr, pixelsPerUnit, gradX = randomGrad(), gradY = randomGrad(), texture = 0.0,
                      weight = 1.0, base = randomGrad())

    return Image.merge("RGB", (redPlane, greenPlane, bluePlane))


# Color image re-editing
def reColor(pixelsPerUnit = 250, imageFolder = "images", textFolder = "text", start = 1, level = 8):

    for filename in sorted(os.listdir(textFolder)):
        if filename.endswith('.txt'):
            filePath = os.path.join(textFolder, filename)
            
            try:
                exprData = readText.readFile(filePath)
                image = None

                if isinstance(exprData, dict):
                    print(f"Process in recreating color image")

                    baseName = os.path.splitext(filename)[0]
                    image = reColorEdit(exprData['R'], exprData['G'], exprData['B'], pixelsPerUnit = pixelsPerUnit, level = level)
                    # COLOR001 -> ReCOLOR001 (original image is kept)
                    reName = f"Re{baseName}"
                    finalPath = os.path.join(imageFolder, f"{reName}.png")
                    image.save(finalPath, "PNG")
                    print(f"Saved recreated color image {reName}")

                    
                elif isinstance(exprData, str):
                    print(f"Skip gray file")
                    continue
        
            

            except Exception:
                print(f"Error processing!!")
                
    return None


# Input level from the user
def editLevel():
    print("-- Set up levels --")
    while True:
        try:
            level = input("For re-editing choose a level (4-8): ").strip()
            if not level:
                level = 8
            level = int(level)
            if 4 <= level <= 8:
                print(f"Re-editing level: {level}")
                return level
            print("Choose one of levels from 4 to 8.")
        except ValueError:
            print("It is not available number.")
    



































    
