#
# Mingyo Mplay
#
# Description: from images folder, try to play in Houdini's mplay
#
# Author: Mingyo Heo
# Date: oct 19, 2025
#
# input: getting images folder path. mplay is found automatically
#        (PATH, $HFS, default Houdini install folders on Mac / Windows / Linux).
#        If it cannot be found, the user inputs the mplay path.
# output: images sequence play in mplay
#



import os
import sys
import glob
import shutil
import subprocess


# mplay
def mplayExeName():
    if sys.platform.startswith("win"):
        return "mplay.exe"
    return "mplay"


# Default Houdini install locations per OS
def candidatePaths():
    exe = mplayExeName()
    patterns = []

    hfs = os.environ.get("HFS")
    if hfs:
        patterns.append(os.path.join(hfs, "bin", exe))

    if sys.platform == "darwin":
        patterns.append("/Applications/Houdini/Current/Frameworks/Houdini.framework/Versions/Current/Resources/bin/mplay")
        patterns.append("/Applications/Houdini/Houdini*/Frameworks/Houdini.framework/Versions/Current/Resources/bin/mplay")
    elif sys.platform.startswith("win"):
        for root in [os.environ.get("ProgramFiles", r"C:\Program Files"), r"C:\Program Files"]:
            patterns.append(os.path.join(root, "Side Effects Software", "Houdini*", "bin", exe))
    else:
        patterns.append("/opt/hfs*/bin/mplay")

    found = []
    for pattern in patterns:
        
        for path in sorted(glob.glob(pattern), reverse=True):
            if path not in found:
                found.append(path)
    return found


# Check the file is a runnable mplay
def isExecutable(path):
    return bool(path) and os.path.isfile(path) and os.access(path, os.X_OK)


# Find the path to mplay
def mplayInput():

    # 1. mplay in PATH
    inPath = shutil.which("mplay")
    if inPath:
        return inPath

    # 2. Default Houdini install folders
    for path in candidatePaths():
        if isExecutable(path):
            return path

    # 3. Input direct path
    while True:
        print("Put your computer's Houdini mplay file path.")
        if sys.platform.startswith("win"):
            print(r"e.g.: C:\Program Files\Side Effects Software\Houdini 21.0.440\bin\mplay.exe")
        else:
            print("e.g.: /Applications/Houdini/Houdini21.0.440/Frameworks/Houdini.framework/Versions/Current/Resources/bin/mplay")

        try:
            mplayPath = input("mplay file path (empty to cancel): ").strip().strip('"').strip("'")
        except EOFError:
            print("No input. Skip mplay.")
            return None

        if not mplayPath:
            return None

        mplayPath = os.path.expanduser(mplayPath)

        # User put Houdini folder instead of the mplay file
        if os.path.isdir(mplayPath):
            for sub in [os.path.join("bin", mplayExeName()),
                        os.path.join("Frameworks", "Houdini.framework", "Versions", "Current", "Resources", "bin", "mplay")]:
                if isExecutable(os.path.join(mplayPath, sub)):
                    mplayPath = os.path.join(mplayPath, sub)
                    break

        # Check the path available or not
        if isExecutable(mplayPath):
            print("Prepare to play in mplay...")
            return mplayPath

        print("Error!! Check the path again.")


# Play mplay the images sequence
def mplay(prefix = "", suffix = ".png", imageFolder = "images"):

    imageFolder = os.path.abspath(imageFolder)

    # Find image files from "images" folder
    try:
        play = os.listdir(imageFolder)
    except FileNotFoundError:
        print(f"Error! Folder '{imageFolder}' not found.")
        return

    # Sorted -> frames play in order on every OS
    filePath = [os.path.join(imageFolder, fileName)
                for fileName in sorted(play)
                if fileName.endswith(suffix) and fileName.startswith(prefix)]

    if not filePath:
        print(f"No found images '{prefix}*{suffix}' in '{imageFolder}'.")
        return

    mplayCommand = mplayInput()
    if not mplayCommand:
        print("mplay not found. Skip playing.")
        return

    print(f"Work in mplay: {mplayCommand}")

    # List arguments: no shell, so spaces / quotes in paths are safe on every OS
    try:
        result = subprocess.run([mplayCommand] + filePath)
    except OSError as e:
        print(f"We cannot run mplay: {mplayCommand} ({e})")
        return

    if result.returncode != 0:
        print(f"mplay exited with code {result.returncode}")
