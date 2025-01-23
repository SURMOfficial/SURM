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

cmd_pts = "($/GFX/Resources/Resource_CommandPoints, "
# rd_bonus_str = "SpeedBonusOnRoad ="
tickets = "($/GFX/Resources/Resource_Tickets, "
def replace(file_path, cmd_pts, tickets):
    #Create temp file
    fh, abs_path = mkstemp()
    # subst = cmd_pts
    # rd_str = tickets
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file: #this just deletes everything, unclear why it was because I had already opened it (causes some kind of conflict)
            for line in old_file:
                # print(line)
                
                x = line.find(cmd_pts)
                if x != -1:
                    points = re.findall(r'\d+',line)
                    points = int(points[0])
                    
                # x = line.find(tickets)
                # if x != -1:
                #     rd_bonus = re.findall(r'\d+\.\d+',line)    
                #     rd_bonus = float(rd_bonus[0])
                x = line.find(tickets)
                if x != -1:
                    # rd_spd = round(res_spd*(1+rd_bonus)/(1000*(2901/370)/(3600)))
                    subst = "                        " + tickets + str(points) + "),\n"
                    orig = line
                    new_file.write(line.replace(orig, subst))
                else:
                    new_file.write(line)
                        
                    # rd_str = re.findall('\d+',line)
                    # rd_str = real_rd + rd_str[0]
                    
                
        #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


replace(filpath, cmd_pts, tickets)