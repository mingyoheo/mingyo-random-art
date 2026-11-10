#
# Mingyo Read File
#
# Description: a module for read text files which are saved matematical expressions for generating images,
# depending on the image type(Gray or Color), return to data by putting proper forms.
#
# Author: Mingyo Heo
# Date: oct 19, 2025
#
# input: get text file pathes
# output: Gray image gets simplicity expressions and Color image gets r, g, b expressions
#




import os

# Read expression content from a file path
def readFile(filePath):
    exprs = {}
    with open(filePath, "r") as f:

        lines = [line.strip() for line in f if line.strip()]

        if not lines:
            raise ValueError("No found the file.")

        imgType = lines[0]

        # Gray image type
        if imgType == "Gray" and len(lines) >= 2:
            return lines[1]

        # Color image type
        elif imgType == "Color" and len(lines) >= 4:

            rPart = lines[1].split(':', 1)
            if len(rPart) > 1:
                exprs['R'] = rPart[1].strip()

            gPart = lines[2].split(':', 1)
            if len(gPart) > 1:
                exprs['G'] = gPart[1].strip()

            bPart = lines[3].split(':', 1)
            if len(bPart) > 1:
                exprs['B'] = bPart[1].strip()
                
            return exprs
        else:
            raise ValueError(f"{filePath} numerical expressions are incorrect!!")





















        
