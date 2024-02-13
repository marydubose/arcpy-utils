# Mary DuBose
# June 15, 2023
# Process flood inundation shapefiles to get count of buildings affected

import arcpy
import os
import shutil

base_dir = r"S:\Tech\medubose\Flood_Trigger"
new_dir = r"S:\Tech\medubose\Flood_Trigger\Inun_Shapefiles_2"
inun_gdb = r"S:\Tech\medubose\Flood_Trigger\Inun_Singlepart.gdb"

levels = {"1": "50", "2": "100", "3": "500", "4": "1000", "5": "Germantown"}

print("Copying and renaming shapefiles...")
for dir in os.listdir(base_dir):
	if dir.startswith("Small5"):
		flood_lvl = levels[dir[-1]]
		dir_full = os.path.join(base_dir, dir)
		
		for subdir in os.listdir(dir_full):
			parts = subdir.split("_")
			basin = parts[-1]
			basin = basin.replace("&", "")	
			newname = basin + "_" + flood_lvl
			
			subdir_full = os.path.join(dir_full, subdir)
		
			for file in os.listdir(subdir_full):
				oldpath = os.path.join(subdir_full, file)
				ext = file[-4:]
				newfile = newname + ext
				newpath = os.path.join(new_dir, newfile)
				print(oldpath)
				print(newpath)
				shutil.copy2(oldpath, newpath)
			
print("Splitting shapefiles into singlepart features...")
for shpfile in os.listdir(new_dir):
	if shpfile.endswith("shp"):
		shppath = os.path.join(new_dir, shpfile)
		gdbpath = os.path.join(inun_gdb, shpfile[:-4])
		arcpy.MultipartToSinglepart_management(shppath, gdbpath)
		

streams = r"S:\Tech\medubose\Flood_Trigger\Flood_GIS.gdb\streams_ft"
bldgs = r"S:\Tech\medubose\Flood_Trigger\Flood_GIS.gdb\WR_buildings"
basins = r"S:\Tech\medubose\Flood_Trigger\Flood_GIS.gdb\WolfRiver_Subbasins"
basin_gdb = r"S:\Tech\medubose\Flood_Trigger\Basins_Split.gdb"
results = r"S:\Tech\medubose\Flood_Trigger\Inun_Results.gdb"

arcpy.MakeFeatureLayer_management(bldgs, "bldg_lyr")

print("Splitting basin layer...")
arcpy.analysis.SplitByAttributes(basins, basin_gdb, ["BasinName"])
logtext = ""
		
arcpy.env.workspace = inun_gdb

i = 0

for fc in arcpy.ListFeatureClasses():
	result = fc + "_count"
	result_path = os.path.join(results, result)
	if arcpy.Exists(result_path):
		continue
	
	print("Selecting polygons near streams...")
	fc_path = os.path.join(arcpy.env.workspace, fc)
	lyrname = fc + "_lyr"
	arcpy.MakeFeatureLayer_management(fc_path, lyrname)
	arcpy.SelectLayerByLocation_management(lyrname, "INTERSECT", streams, "", "NEW_SELECTION")
	
	print("Selecting buildings in flood zone...")
	arcpy.SelectLayerByLocation_management("bldg_lyr", "INTERSECT", lyrname, "", "NEW_SELECTION")
	
	basin = fc.split("_")[0]
	basin_select = os.path.join(basin_gdb, basin)
	basinname = basin + str(i) + "_lyr"
	arcpy.MakeFeatureLayer_management(basin_select, basinname)
	
	print("Subselection of buildings within basin...")
	arcpy.SelectLayerByLocation_management("bldg_lyr", "INTERSECT", basinname, "", "SUBSET_SELECTION")
	
	arcpy.CopyFeatures_management("bldg_lyr", result_path)
	count = arcpy.GetCount_management("bldg_lyr")[0]
	text = basin + ": " + count + " buildings\n"
	logtext += text
	
	arcpy.SelectLayerByAttribute_management("bldg_lyr", "CLEAR_SELECTION")
	i += 1
	
with open(r"S:\Tech\medubose\Flood_Trigger\Bldg_Count_2.txt", "w") as outfile:
	outfile.write(logtext)