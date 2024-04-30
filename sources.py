# -*- coding: utf-8 -*-
#                           ██╗██████╗ ██╗           
#                           ██║╚════██╗██║           
#                           ██║ █████╔╝██║           
#                      ██   ██║██╔═══╝ ██║           
#                      ╚█████╔╝███████╗███████╗      
#                       ╚════╝ ╚══════╝╚══════╝      
#                       https://jusdeliens.com
#
# Designed with 💖 by Jusdeliens
# Under CC BY-NC-ND 3.0 licence 
# https://creativecommons.org/licenses/by-nc-nd/3.0/ 

import os
import base64
import logger as anx

def exploreSourcesDirs(rootpath:str, subdirs=[], takeOnlyExts=['.py','.json'], dontTakeExts=[], dontTakeFolders=["venv", "j2l"], takeHidden=False, recursive=True, explored={}):
    dirpath = os.path.join(rootpath, *subdirs)
    filenames = os.listdir(dirpath)
    for filefullname in filenames:
        filefullpath = os.path.join(dirpath, filefullname)
        filename, fileext = os.path.splitext(filefullname)
        if ( fileext in dontTakeExts ):
            continue # Not blacklist exts
        if ( len(fileext) > 0 and len(takeOnlyExts) > 0 and fileext not in takeOnlyExts ):
            continue # Only whitelist exts
        if ( recursive == False and len(fileext) == 0 ):
            continue # Recursive folder
        if ( len(filename) >= 2 and filename[0] == "." and filename[1] != "." and takeHidden == False):
            continue # No hidden folder
        if ( filename in dontTakeFolders and len(fileext) == 0 ):
            continue # No env folder
        if ( len(filename) >= 2 and filename[0] == "_" and filename[1] == "_" and takeHidden == False):
            continue # No hidden folder
        if ( len(fileext) == 0 ): # Recursive folder explore
            subdirsRecursive = subdirs.copy()
            subdirsRecursive.append(filefullname)
            exploreSourcesDirs(rootpath, subdirsRecursive, takeOnlyExts, dontTakeExts, dontTakeFolders, takeHidden, recursive, explored)
        else:
            with open(filefullpath, "r", encoding="utf-8") as src:
                explored[filefullpath.replace(rootpath, "")] = (
                    subdirs,
                    filename, fileext, 
                    os.path.getctime(filefullpath), 
                    os.path.getmtime(filefullpath), 
                    (base64.b64encode(src.read().encode('utf-8'))).decode('utf-8')
                )
    return explored

def fetchSources(dirpath:str|None=None, entryFile="main.py"):
    if ( dirpath == None ):
        dirpath = os.path.dirname(os.path.abspath(__file__))
    # Find main.py
    depth, maxdepth = 0,3
    while depth < maxdepth:
        filenames = os.listdir(dirpath)
        if ( entryFile in filenames ):
            break
        depth += 1
        dirpath = os.path.join(dirpath, "..")
    if ( depth == maxdepth ):
        anx.debug(f"{entryFile} not found")
        return None
    anx.debug(f"Found {entryFile} at depth "+str(-depth))
    # Explorer all folders from main.py
    srcs = exploreSourcesDirs(dirpath)
    return srcs
