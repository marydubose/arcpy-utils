# Mary DuBose
# 3/1/2022
# This script assigns values to the SITE_ID field for the VSS data.

import arcpy

arcpy.env.workspace = r"S:\Admin\backups\vss\VSS_2021_Backups\20220301\VSS_Data_Final.gdb"

fcs = arcpy.ListFeatureClasses()

abbreviations = {'channel_alteration': 'CA',
				 'erosion_site': 'ER',
				 'inadequate_buffer': 'IB',
				 'pipe_outfall': 'PO',
				 'stream_construction': 'SC',
				 'trash_dumping': 'TD',
				 'unusual_condition_comment': 'UC',
				 'representative_site': 'RS',
				 'fish_barrier': 'FB',
				 'exposed_pipe': 'EP'}
				 

for fc in fcs:
	index = 1
	with arcpy.da.UpdateCursor(fc, ["SITE_ID"]) as cursor:
		for row in cursor:
			site_id = abbreviations[fc] + '_' + str(index).zfill(5)
			row[0] = site_id
			cursor.updateRow(row)
			index += 1