# Mary DuBose
# May 20, 2022
# This script generates summary tables for rep sites per reach for the VSS final report.

import arcpy
import os
import statistics
import xlwt
from itertools import groupby

# critical impairment tables
# select all impairments within a polygon where severity = 1
# write results to Excel
# columns needed: 
# - Site ID
# - Severity
# - Comments 

arcpy.env.workspace = r"C:\workspace\VSS\Final_Report.gdb"

ca = os.path.join(arcpy.env.workspace, "channel_alteration")
arcpy.MakeFeatureLayer_management(ca, "ca_fc")
ep = os.path.join(arcpy.env.workspace, "exposed_pipe")
arcpy.MakeFeatureLayer_management(ep, "ep_fc")
er = os.path.join(arcpy.env.workspace, "erosion_site")
arcpy.MakeFeatureLayer_management(er, "er_fc")
fb = os.path.join(arcpy.env.workspace, "fish_barrier")
arcpy.MakeFeatureLayer_management(fb, "fb_fc")
ib = os.path.join(arcpy.env.workspace, "inadequate_buffer")
arcpy.MakeFeatureLayer_management(ib, "ib_fc")
po = os.path.join(arcpy.env.workspace, "pipe_outfall")
arcpy.MakeFeatureLayer_management(po, "po_fc")
td = os.path.join(arcpy.env.workspace, "trash_dumping")
arcpy.MakeFeatureLayer_management(td, "td_fc")
uc = os.path.join(arcpy.env.workspace, "unusual_condition_comment")
arcpy.MakeFeatureLayer_management(uc, "uc_fc")

impairment_fls = ["ca_fc", "ep_fc", "er_fc", "fb_fc", "ib_fc", "po_fc", "td_fc", "uc_fc"]

polygons = os.path.join(arcpy.env.workspace, "reach_polygons")
arcpy.MakeFeatureLayer_management(polygons, "poly_fc")

impairment_fields = ["SITE_ID", "SEVERITY", "COMMENTS"]

with arcpy.da.SearchCursor(polygons, ["reach_name", "reach_id"]) as scur:
	for row in scur:
		rid = row[1]
		sql = """ reach_id = '{r}' """.format(r=rid)
		arcpy.management.SelectLayerByAttribute("poly_fc", "NEW_SELECTION", sql)
	
		critical_impairments = []
		
		for imp in impairment_fls:
			arcpy.management.SelectLayerByLocation(imp, "INTERSECT", "poly_fc", "", "NEW_SELECTION", "")
			sql2 = """ SEVERITY = 1 """
			arcpy.management.SelectLayerByAttribute(imp, "SUBSET_SELECTION", sql2)
			with arcpy.da.SearchCursor(imp, impairment_fields) as icur:
				for irow in icur:
					ids = [item[0] for item in critical_impairments]
					if str(irow[0]) not in ids:
						impairment_data = []
						impairment_data.append(str(irow[0]))
						impairment_data.append(str(irow[1]))
						if irow[2] is not None:
							impairment_data.append(irow[2].encode('utf-8'))
						else:
							impairment_data.append(str(irow[2]))

						critical_impairments.append(impairment_data)
		
		critical_impairments.sort()
		
		excel_name = row[0] + "_" + row[1] + ".xls"
		excel_folder = r"C:\workspace\vss\critical_impairment_tables"
		excel_out = os.path.join(excel_folder, excel_name)

		wb = xlwt.Workbook(encoding="utf8")

		ws = wb.add_sheet("Sheet1")
		ws.write(0, 0, "Site ID")
		ws.write(0, 1, "Severity")
		ws.write(0, 2, "Comments")
		
		row = 1
		for impairment in critical_impairments:
			ws.write(row, 0, impairment[0])
			ws.write(row, 1, impairment[1])
			ws.write(row, 2, impairment[2])
			row += 1
		
		wb.save(excel_out)
		