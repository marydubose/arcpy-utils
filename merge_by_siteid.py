# Mary DuBose
# June 24, 2022
# This script merges features with the same Site ID into multipart features.

import arcpy
import os

arcpy.env.workspace = r"S:\Water_Projects\Shelby_County\VisualStreamAssessment\Data\Processing\LinearReference\LR_output.gdb"
new_gdb = r"S:\Water_Projects\Shelby_County\VisualStreamAssessment\Data\Processing\Merge\VSA.gdb"

fcs = arcpy.ListFeatureClasses()

to_skip = ["representative_site", "stream_routes"]

edit = arcpy.da.Editor(r"S:\Water_Projects\Shelby_County\VisualStreamAssessment\Data\Processing\LinearReference\LR_output.gdb")
edit.startEditing(False, True)
edit.startOperation()

for fc in fcs:
	if fc not in to_skip:
		new_fc = os.path.join(new_gdb, fc)
		arcpy.MakeFeatureLayer_management(fc, templayer)
		arcpy.Dissolve_management(templayer, new_fc, "SITE_ID")
		
edit.stopOperation()
edit.stopEditing(True)