import arcpy

roads = r"C:\workspace\workspace\Default.gdb\ROAD_Dissolve"
intersections = r"C:\workspace\workspace\Default.gdb\ROAD_Dissolve_Intersect"

arcpy.MakeFeatureLayer_management(roads, "RoadsFL")
arcpy.MakeFeatureLayer_management(intersections, "IntersectionsFL")

with arcpy.da.UpdateCursor(intersections, ("OBJECTID", "Street1", "Street2")) as ucur:
	for row in ucur:
		oid = row[0]
		sql = """ OBJECTID = {id} """.format(id=oid)
		arcpy.SelectLayerByAttribute_management("IntersectionsFL", "NEW_SELECTION", sql)
		arcpy.SelectLayerByLocation_management("RoadsFL", "INTERSECT", "IntersectionsFL", 0, "NEW_SELECTION")
		street1 = ""
		street2 = ""
		bearing1 = ""
		with arcpy.da.SearchCursor("RoadsFL", ("LABEL", "bearing")) as scur:
			for srow in scur:
				st = srow[0]
				dir = float(srow[1])
				if street1 == "":
					street1 = st
					bearing1 = dir
				else:
					if abs(bearing1-dir) > 20:
						street2 = st
		row[1] = street1
		row[2] = street2
		ucur.updateRow(row)				
		

