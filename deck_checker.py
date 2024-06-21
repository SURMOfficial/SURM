# -*- coding: utf-8 -*-
"""
Created on Sun May 26 11:35:40 2024

@author: tevis
"""

import re
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

filpath_unit = r"C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\SURM\GameData\Generated\Gameplay\Decks\Decks.txt"
filpath_dpacks = r"C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\SURM\GameData\Generated\Gameplay\Decks\DeckPacks.txt"
filpath_dpacks_extra = r"C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\SURM\GameData\Generated\Gameplay\Decks\DeckPacks_extra.txt"
# f = open(filpath,"w")

u_cutofft = len('\t\t\tTransport = $/GFX/Unit/Descriptor_Unit_')
u_cutoffs = len('            Transport = $/GFX/Unit/Descriptor_Unit_')
XP = "ExperienceLevel"
transp = 'Transport'
# rd_bonus_str = "SpeedBonusOnRoad ="
# tickets = "($/GFX/Resources/Resource_Tickets, "
def replace(filpath_unit,filpath_dpacks,filpath_dpacks_extra):
    #Create temp file
    fh, abs_path = mkstemp()
    # subst = cmd_pts
    # rd_str = tickets
    append = False
    transchk = False
    level = -1
    list_unit = []
    with open(filpath_unit) as unit_file:
        for line_unit in unit_file:
            x = line_unit.find('Descriptor_Deck_Pack_')
            if x != -1:
                test_line = line_unit[10:-2]
                with open(filpath_dpacks) as pack_file: #this just deletes everything, unclear why it was because I had already opened it (causes some kind of conflict)
                    content = pack_file.read()
                    # check if string present or not
                    if test_line not in content:
                        # print(test_line +' exist')
                    # else:
                        list_unit.append(test_line)
    list_unit = list(set(list_unit))                    
                        # print(test_line +' does not exist')
    with fdopen(fh,'w') as new_file:
        for lu in list_unit:
            line_in = 'Descriptor_Deck_Pack_' + lu + ' is DeckPackDescriptor\n'
            new_file.write(line_in)
            new_file.write('(\n')
            # if lu=='Descriptor_Deck_Pack_Grenzer_Mot_DDR_PSzH_IV_DDR_':
            #     print('help')
            print(lu)
            XP = int(lu[-1])
            if XP != 0:
                line_in = '    Xp = ' + str(XP) + '\n'
                new_file.write(line_in)
            country = lu[-5:-3]
            u_end = lu.find(country)+3
            unit = lu[21:u_end]
            
            # transport
            if len(lu)>u_end+2:
                transport = lu[u_end+1:-2]
                line_in = '    Transport = $/GFX/Unit/Descriptor_Unit_' + transport +'\n'
                new_file.write(line_in)

            line_in = '    Unit = $/GFX/Unit/Descriptor_Unit_' + unit +'\n'
            new_file.write(line_in)
            new_file.write(')\n')
            new_file.write('\n')
# Descriptor_Deck_Pack_81mm_mortar_UK is DeckPackDescriptor
# (
#     Unit = $/GFX/Unit/Descriptor_Unit_81mm_mortar_UK
# )

        # for line_pack in pack_file:
            #     # print(line)
                
            #     x = line.find(XP)
            #     if x != -1:
            #         level = re.findall(r'\d+',line)
            #         level = int(level[0])
            #         append = True
            #     elif append:
            #         line_lev = line[:-1]+'_'+str(level)+line[-1:]
            #         # orig = line
            #         # new_file.write(line.replace(orig, line_lev))
            #         append = False
            #         transchk = True
            #     elif transchk:

            #         x1 = line.find(transp)
            #         if x1 != -1:
            #             if line[0:3] == '\t\t\t':
            #                 u_cutoff = u_cutofft
            #             elif line[0:12] == '            ':
            #                 u_cutoff = u_cutoffs
            #             else:
            #                 print('ERROR')
                        
            #             unit = line[u_cutoff:-1]
            #             line_lev_u = line_lev[:-3]+'_'+unit+line_lev[-3:]
            #         else:
            #             line_lev_u = line_lev
            #         new_file.write(line_lev_u)
            #         transchk = False
            #     else:
            #         new_file.write(line)
                
                
                
            #     # x = line.find(tickets)
            #     # if x != -1:
            #     #     rd_bonus = re.findall(r'\d+\.\d+',line)    
            #     #     rd_bonus = float(rd_bonus[0])
            #     # x = line.find(tickets)
                # if x != -1:
                #     # rd_spd = round(res_spd*(1+rd_bonus)/(1000*(2901/370)/(3600)))
                #     subst = "                        " + tickets + str(points) + "),\n"
                #     orig = line
                #     new_file.write(line.replace(orig, subst))
                
                        
                    # rd_str = re.findall('\d+',line)
                    # rd_str = real_rd + rd_str[0]
                    
                
        #Copy the file permissions from the old file to the new file
    copymode(filpath_dpacks_extra, abs_path)
    #Remove original file
    remove(filpath_dpacks_extra)
    #Move new file
    move(abs_path, filpath_dpacks_extra)

replace(filpath_unit,filpath_dpacks,filpath_dpacks_extra)