# -*- coding: utf-8 -*-
"""
Created on Sun May 26 11:35:40 2024

@author: tevis
"""

import re
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

filpath = r'C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\SURM\GameData\Generated\Gameplay\Decks\Deck_update.txt'

# f = open(filpath,"w")

u_cutofft = len('\t\t\tTransport = $/GFX/Unit/Descriptor_Unit_')
u_cutoffs = len('            Transport = $/GFX/Unit/Descriptor_Unit_')
XP = "ExperienceLevel"
transp = 'Transport'
# rd_bonus_str = "SpeedBonusOnRoad ="
# tickets = "($/GFX/Resources/Resource_Tickets, "
def replace(file_path, XP,transp,u_cutofft,u_cutoffs):
    #Create temp file
    fh, abs_path = mkstemp()
    # subst = cmd_pts
    # rd_str = tickets
    append = False
    transchk = False
    level = -1
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file: #this just deletes everything, unclear why it was because I had already opened it (causes some kind of conflict)
            for line in old_file:
                # print(line)
                
                x = line.find(XP)
                if x != -1:
                    level = re.findall(r'\d+',line)
                    level = int(level[0])
                    append = True
                elif append:
                    line_lev = line[:-1]+'_'+str(level)+line[-1:]
                    # orig = line
                    # new_file.write(line.replace(orig, line_lev))
                    append = False
                    transchk = True
                elif transchk:

                    x1 = line.find(transp)
                    if x1 != -1:
                        if line[0:3] == '\t\t\t':
                            u_cutoff = u_cutofft
                        elif line[0:12] == '            ':
                            u_cutoff = u_cutoffs
                        else:
                            print('ERROR')
                        
                        unit = line[u_cutoff:-1]
                        line_lev_u = line_lev[:-3]+'_'+unit+line_lev[-3:]
                    else:
                        line_lev_u = line_lev
                    new_file.write(line_lev_u)
                    transchk = False
                else:
                    new_file.write(line)
                
                
                
                # x = line.find(tickets)
                # if x != -1:
                #     rd_bonus = re.findall(r'\d+\.\d+',line)    
                #     rd_bonus = float(rd_bonus[0])
                # x = line.find(tickets)
                # if x != -1:
                #     # rd_spd = round(res_spd*(1+rd_bonus)/(1000*(2901/370)/(3600)))
                #     subst = "                        " + tickets + str(points) + "),\n"
                #     orig = line
                #     new_file.write(line.replace(orig, subst))
                
                        
                    # rd_str = re.findall('\d+',line)
                    # rd_str = real_rd + rd_str[0]
                    
                
        #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


replace(filpath, XP, transp,u_cutofft,u_cutoffs)