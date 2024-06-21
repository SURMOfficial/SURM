# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 18:57:12 2024

@author: tevis
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 19:57:06 2024

@author: tevis
"""

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

filpath_dest = r'C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\BugHunt\UniteDescriptor_txt.txt'
filpath_origin = r'C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\SURM\UniteDescriptor_txt.txt'
# entries = ['TemplateUnitCriticalModule',
#             'ResistanceFront ',
#             'ResistanceSides ',
#             'ResistanceRear ',
#             'ResistanceTop ',
#             'HitRollSize ',
#             'MaxSpeed ',
#             'VitesseCombat ',
#             'SpeedBonusOnRoad ',
#             'MaxAcceleration ',
#             'MaxDeceleration ',
#             'TempsDemiTour ',
#             'StartTime ',
#             'StopTime ',
#             'RotationStartTime ',
#             'RotationStopTime ',
#             'OpticsAltitudeConfig ',
#             'PorteeVisionTBA ',
#             'PorteeVisionFOW ',
#             'DetectionTBA',
#             'PorteeVision ',
#             'PorteeIdentification ',
#             'OpticalStrength ',
#             'OpticalStrengthAltitude ',
            # '( EVisionUnitType/AlwaysInHighAltitude,',
            #  'FuelMoveDuration ', #next test starts here
            #  'IdentifyBaseProbability ',
            #  'TimeBetweenEachIdentifyRoll '
            # '($/GFX/Resources/Resource_CommandPoints, ',
            # 'NbSeatsAvailable ',
            # 'WreckUnloadPhysicalDamageBonus ',
            # 'NbSeatsOccupied '
            # 'ExperienceLevelsPackDescriptor ',
            # 'UnitConcealmentBonus ',
            # 'SuppressDamageLevelsPack ',
            # 'TimeToLoad ',
            # 'RealRoadSpeed ',
            # 'EvacuationTime ',
            # 'StunDamageLevelsPack '
            # 'Altitude ',
            # 'AltitudeMin ',
            # 'Speed ',
            # 'AgilityRadius ',
            # 'PitchAngle ',
            # 'RollAngle ',
            # 'RollSpeed ',
            # 'EvacAngle ',
            # 'HitRollECM ',
            # 'SupplyCapacity ',
            # 'MaxDistanceForOffensiveReaction ',
            # 'LowAltitudeFlyingAltitude ',
            # 'NearGroundFlyingAltitude ',]

# entries = ['PorteeVisionTBA ',
#             'PorteeVisionFOW ',
#             'PorteeVision ']
entries = [ 'DefaultSkillList ',]

# entries = ['ResistanceFront','ResistanceSides',]


# f = open(filpath,"w")

# mesh_str = "ReferenceMesh = "
# bhole = "ProjectileModelResource = "
#  Descriptor_Unit_2K12_KUB_DDR
def copyoverlist(filpath_dest,filpath_origin, entries, find_unit = 'export'):
    #Create temp file
    for entry in entries:
        fh, abs_path = mkstemp()
        
        # with fdopen(fh,'w') as new_file:
        with open(filpath_dest,'r') as dest_file: #this just deletes everything, unclear why it was because I had already opened it (causes some kind of conflict)
            get_all_dest=dest_file.readlines()  
        with open(filpath_origin,'r') as orig_file: #this just deletes everything, unclear why it was because I had already opened it (causes some kind of conflict)
            get_all_origin=orig_file.readlines()  
        with fdopen(fh,'w') as new_file:
                print(entry)
                inlist = False
                insertlist = False
                inserted = False
                resume_cp = True
                for line in get_all_dest:
                    # print(entry+line)
                    x = line.find(find_unit)
                    
                    
                    # entry_cp = 'WTF'
                    if x != -1:
                        unit = line
                    x = line.find(entry)
                    if x != -1:
                        inlist = True #I don't think I need this flag
                        list_entries =''
                        start_list = False
                    # assemble the entire list from the source file
                        print(entry + unit)
                        u_find_flag = False
                        # replace = True
                        for line_o in get_all_origin:
                            if not u_find_flag:
                                x = line_o.find(unit)
                                if x != -1:
                                    u_find_flag = True
                            else:
                                x = line_o.find(entry)
                                if x != -1:
                                    start_list = True
                                    list_entries = line_o
                                    # entry_cp = line_o
                                    # u_find_flag = False
                                    # break
                                elif start_list:
                                    list_entries+=line_o
                                if line_o.find(']') != -1 and start_list:
                                    start_list = False
                                    insertlist = True
                                    break
                    
                    # if copy_direct:
                    #     new_file.write(line)
                    if insertlist:
                        new_file.write(list_entries)
                        resume_cp = False
                        insertlist = False
                        inserted = True
                    if resume_cp:
                        new_file.write(line)
                    if inserted and line.find(']') != -1 :
                        resume_cp = True
                        inserted = False
                        inlist = False
                    
                    # x = line.find(entry)
                    
                        # replace = False
                    # else:
                    #     new_file.write(line)
        copymode(filpath_dest, abs_path)
            #Remove original file
        remove(filpath_dest)
            #Move new file
        move(abs_path, filpath_dest)
    # with open(file_path,'w') as old_file: #this just deletes everything, unclear why it was because I had already opened it (causes some kind of conflict) 
    #     for line in reversed(get_all):
    #         # print(line)
    #         x = line.find(bhole)
    #         if x != -1:
    #             subst = pattern + line[x+len(bhole):-1]
    #         old_file.write(line.replace(pattern, subst))
        #Copy the file permissions from the old file to the new file



copyoverlist(filpath_dest,filpath_origin,entries)