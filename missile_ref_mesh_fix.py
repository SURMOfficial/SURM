# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 09:13:43 2023

@author: tevis
"""

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

filpath = r'C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\SURM\GameData\MissileDescriptors_txt.txt'

# f = open(filpath,"w")

mesh_str = "ReferenceMesh = $/GFX/DepictionResources/Modele_"
bhole = "BlackHoleIdentifier = "

def replace(file_path, pattern, bhole):
    #Create temp file
    fh, abs_path = mkstemp()
    subst = pattern
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file: #this just deletes everything, unclear why it was because I had already opened it (causes some kind of conflict)
            for line in old_file:
                # print(line)
                
                x = line.find(bhole)
                if x != -1:
                    subst = pattern + line[x+len(bhole)+1:-2]
                new_file.write(line.replace(pattern, subst))
        #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


replace(filpath,mesh_str,bhole)