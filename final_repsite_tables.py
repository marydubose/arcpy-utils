# Mary DuBose
# May 20, 2022
# This script generates summary tables for rep sites per reach for the VSS final report.

import arcpy
import os
import statistics
import xlwt
from itertools import groupby

# rep site summary tables
# select all rep sites within a polygon
# write results to Excel?
# calculate min, max, and median for multiple fields:
# - riffle width, depth, and percentage
# - run width, depth, and percentage
# - pool width, depth, and percentage
# - bank height
# - high water mark
# calculate proportion of rep sites with each primary bottom type

# critical impairment tables
# select all impairments within a polygon where severity = 1
# write results to Excel
# columns needed: 
# - Site ID
# - Severity
# - Comments 

arcpy.env.workspace = r"C:\workspace\VSS\Final_Report.gdb"

repsites = os.path.join(arcpy.env.workspace, "representative_site")
arcpy.MakeFeatureLayer_management(repsites, "repsite_fc")
polygons = os.path.join(arcpy.env.workspace, "reach_polygons")
arcpy.MakeFeatureLayer_management(polygons, "poly_fc")

repsite_fields = ["BANK_HEIGHT", "HIGH_WATER_MARK", "BOTTOM_TYPE_PRI", "WETTED_WIDTH_RIFFLES", "THALWEG_DEPTH_RIFFLES", /
					"RIFFLE_PERCENT_REACH", "WETTED_WIDTH_RUNS", "THALWEG_DEPTH_RUNS", "RUNS_PERCENT_REACH",  /
					"WETTED_WIDTH_POOLS", "THALWEG_DEPTH_POOLS", "POOLS_PERCENT_REACH"]

with arcpy.da.SearchCursor(polygons, ["reach_name", "reach_id"]) as scur:
	for row in scur:
		rid = row[1]
		sql = """ reach_id = '{r}' """.format(r=rid)
		arcpy.management.SelectLayerByAttribute(poly_fc, "NEW_SELECTION", sql)
		arcpy.management.SelectLayerByLocation(repsite_fc, "INTERSECT", poly_fc, "NEW_SELECTION")
		
		riffle_width = []
		riffle_depth = []
		riffle_percent = []
		run_width = []
		run_depth = []
		run_percent = []
		pool_width = []
		pool_depth = []
		pool_percent = []
		bank_height = []
		high_water_mark = []
		bottom_type = []
		
		with arcpy.da.SearchCursor(repsite_fc, repsite_fields]) as rcur:
			for rrow in rcur:
				bank_height.append(float(rrow[0]))
				high_water_mark.append(float(rrow[1]))
				bottom_type.append(str(rrow[2]))
				riffle_width.append(float(rrow[3]))
				riffle_depth.append(float(rrow[4]))
				riffle_percent.append(float(rrow[5]))
				run_width.append(float(rrow[6]))
				run_depth.append(float(rrow[7]))
				run_percent.append(float(rrow[8]))
				pool_width.append(float(rrow[9]))
				pool_depth.append(float(rrow[10]))
				pool_percent.append(float(rrow[11]))
				
		riffle_width_min = min(riffle_width)
		riffle_width_max = max(riffle_width)
		riffle_width_median = statistics.median(riffle_width)
		riffle_depth_min = min(riffle_depth)
		riffle_depth_max = max(riffle_depth)
		riffle_depth_median = statistics.median(riffle_depth)
		riffle_percent_min = min(riffle_percent)
		riffle_percent_max = max(riffle_percent)
		riffle_percent_median = statistics.median(riffle_percent)
		
		run_width_min = min(run_width)
		run_width_max = max(run_width)
		run_width_median = statistics.median(run_width)
		run_depth_min = min(run_depth)
		run_depth_max = max(run_depth)
		run_depth_median = statistics.median(run_depth)
		run_percent_min = min(run_percent)
		run_percent_max = max(run_percent)
		run_percent_median = statistics.median(run_percent)
		
		pool_width_min = min(pool_width)
		pool_width_max = max(pool_width)
		pool_width_median = statistics.median(pool_width)
		pool_depth_min = min(pool_depth)
		pool_depth_max = max(pool_depth)
		pool_depth_median = statistics.median(pool_depth)
		pool_percent_min = min(pool_percent)
		pool_percent_max = max(pool_percent)
		pool_percent_median = statistics.median(pool_percent)
		
		bank_height_min = min(bank_height)
		bank_height_max = max(bank_height)
		bank_height_median = statistics.median(bank_height)
		high_water_min = min(high_water_mark)
		high_water_max = max(high_water_mark)
		high_water_median = statistics.median(high_water_mark)
		
		bottoms = {value: len(list(freq)) for value, freq in groupby(sorted(bottom_type))}
		silt_percent = float(bottoms["SILT"])/float(len(bottom_type))
		sand_percent = float(bottoms["SAND"])/float(len(bottom_type))
		gravel_percent = float(bottoms["GRAVEL"])/float(len(bottom_type))
		
		excel_name = row[0] + "_" + row[1] + ".xls"
		excel_folder = r"C:\workspace\vss\repsite_tables"
		excel_out = os.path.join(excel_folder, excel_name)

		wb = xlwt.Workbook()

		ws = wb.add_sheet("Sheet1")
		ws.write(0, 1, "Width Range (Median), feet")
		ws.write(0, 2, "Depth Range (Median), feet")
		ws.write(0, 3, "Percentage Range (Median)")
		ws.write(1, 0, "Riffles")
		ws.write(1, 1, str(riffle_width_min) + " - " + str(riffle_width_max) + " (" + str(riffle_width_median) + ")")
		ws.write(1, 2, str(riffle_depth_min) + " - " + str(riffle_depth_max) + " (" + str(riffle_depth_median) + ")")
		ws.write(1, 3, str(riffle_percent_min) + " - " + str(riffle_percent_max) + " (" + str(riffle_percent_median) + ")")
		ws.write(2, 0, "Runs")
		ws.write(2, 1, str(run_width_min) + " - " + str(run_width_max) + " (" + str(run_width_median) + ")")
		ws.write(2, 2, str(run_depth_min) + " - " + str(run_depth_max) + " (" + str(run_depth_median) + ")")
		ws.write(2, 3, str(run_percent_min) + " - " + str(run_percent_max) + " (" + str(run_percent_median) + ")")
		ws.write(3, 0, "Pools")
		ws.write(3, 1, str(pool_width_min) + " - " + str(pool_width_max) + " (" + str(pool_width_median) + ")")
		ws.write(3, 2, str(pool_depth_min) + " - " + str(pool_depth_max) + " (" + str(pool_depth_median) + ")")
		ws.write(3, 3, str(pool_percent_min) + " - " + str(pool_percent_max) + " (" + str(pool_percent_median) + ")")
		ws.write(4, 1, "Height Range (Median), feet")
		ws.write(4, 2, "Primary Bottom Type")
		ws.write(4, 3, "Percentage of Representative Sites")
		ws.write(5, 0, "Bank Height")
		ws.write(5, 1, str(bank_height_min) + " - " + str(bank_height_max) + " (" + str(bank_height_median) + ")")
		ws.write(5, 2, "Silt")
		ws.write(5, 3, str(silt_percent))
		ws.write(6, 0, "High Water Mark")
		ws.write(6, 1, str(high_water_min) + " - " + str(high_water_max) + " (" + str(high_water_median) + ")")
		ws.write(6, 2, "Sand")
		ws.write(6, 3, str(sand_percent))
		ws.write(7, 2, "Gravel")
		ws.write(7, 3, str(gravel_percent))
		
		wb.save(excel_out)
		
		
				
