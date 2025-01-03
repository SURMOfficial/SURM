# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 09:13:43 2023

@author: tevis
"""
import re
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

filpath = r'C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\SURM\GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf'

# f = open(filpath,"w")

speed_str = "MaxSpeedInKmph ="
rd_bonus_str = "SpeedBonusFactorOnRoad ="
real_rd = "DisplayRoadSpeedInKmph = "
def replace(file_path, speed_str, rd_bonus_str,real_rd):
    #Create temp file
    fh, abs_path = mkstemp()
    subst = real_rd
    rd_str = real_rd
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file: #this just deletes everything, unclear why it was because I had already opened it (causes some kind of conflict)
            for line in old_file:
                # print(line)
                
                x = line.find(speed_str)
                if x != -1:
                    res_spd = re.findall(r'\d+',line)
                    res_spd = float(res_spd[0])
                x = line.find(rd_bonus_str)
                if x != -1:
                    rd_bonus = re.findall(r'\d+\.\d+',line)    
                    rd_bonus = float(rd_bonus[0])
                x = line.find(real_rd)
                if x != -1:
                    rd_spd = round(res_spd*rd_bonus)
                    subst = real_rd + str(rd_spd)
                    rd_str = re.findall('\d+',line)
                    rd_str = real_rd + rd_str[0]
                    
                new_file.write(line.replace(rd_str, subst))
        #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


replace(filpath, speed_str, rd_bonus_str,real_rd)