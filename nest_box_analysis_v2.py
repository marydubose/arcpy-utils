import arcpy
import os
import xlwt

arcpy.env.workspace = r"C:\workspace\workspace\Default.gdb"
# I copied all of the GIS files into a file geodatabase saved on my hard drive
# Change this folder path and the two below to wherever you have your data saved

nests = os.path.join(r"C:\workspace\workspace\Default.gdb", "Nests_All")
near = os.path.join(r"C:\workspace\workspace\Default.gdb", "near_table_nests_3")

near_dict = {}
output = {}

arcpy.MakeFeatureLayer_management(nests, "NestFL")


# The section below is going through the near table to create a list of nearby nests
# It is excluding all nests with a distance of 0 since those are in the same location
print("Building dictionary of nearby nests...")
ncur = arcpy.da.SearchCursor(near, ("IN_FID", "NEAR_FID", "NEAR_DIST"))
for row in ncur:
	in_fid = str(row[0])
	near_fid = str(row[1])
	near_dist = float(row[2])
	data = [near_fid, near_dist]
	if near_dist > 0:
		if in_fid in near_dict:
			near_dict[in_fid].append(data)
		else:
			near_dict[in_fid] = [data]
	else:
		pass
del ncur

# These lines are sorting all the lists of nearby nests from closest to furthest
print("Sorting nests by distance...")
for key, value in near_dict.items():
	value.sort(key=lambda x: x[1])

# This section is to exclude nests that don't overlap in their time range
# It also checks which species the nest is
print("Filtering nests by year, species, and active dates...")	
for key, value in near_dict.items():
	nest = ""
	nestbox = ""
	species = ""
	begin_date = ""
	end_date = ""
	nest2 = ""
	nestbox2 = ""
	species2 = ""
	begin_date_2 = ""
	end_date_2 = ""
	oid = int(key)
	query = """ OBJECTID_1 = {objid} """.format(objid=oid)
	arcpy.management.SelectLayerByAttribute("NestFL", "NEW_SELECTION", query)
	scur = arcpy.da.SearchCursor("NestFL", ("OBJECTID_1", "NESTYEAR", "NESTBOX", "YEAR", "SPECIES", "E1D_MINUS_", "TDAY"))
	for row in scur:
		nest = row[1]
		nestbox = row[2]
		year = int(row[3])
		species = row[4]
		begin_date = int(row[5])
		end_date = int(row[6])
		nest_data = [nest, nestbox, species]
		
	# This section checks to make sure there isn't missing data for the nests
	if species == "" or begin_date == "" or end_date == "":
		print(str(key))
		print("Data not found")
		continue
		
	# This section goes through each possible nearest nest
	# It compares the year, active dates, and species
	for nest in value:
		oid_check = int(nest[0])
		dist = float(nest[1])
		query = """ OBJECTID_1 = {objid} """.format(objid=oid_check)
		arcpy.management.SelectLayerByAttribute("NestFL", "NEW_SELECTION", query)
		scur = arcpy.da.SearchCursor("NestFL", ("OBJECTID_1", "NESTYEAR", "NESTBOX", "YEAR", "SPECIES", "E1D_MINUS_", "TDAY"), query)
		for row in scur:
			nest2 = row[1]
			nestbox2 = row[2]
			year2 = int(row[3])
			species2 = row[4]
			begin_date_2 = int(row[5])
			end_date_2 = int(row[6])
			neighbor_data = [str(dist), str(oid_check), nest2, nestbox2, species2]
			output_data = nest_data + neighbor_data
			print("Nest data:")
			print(nest_data)
			print("Neighbor data:")
			print(neighbor_data)
			print("Output:")
			print(output_data)
			if species2 == "" or begin_date_2 == "" or end_date_2 == "":
				print(str(nest))
				print("Data not found")
				continue
			if year == year2:
				if (end_date >= begin_date_2 and end_date_2 >= begin_date):
					if oid in output:
						output[oid].append(output_data)
					else:
						output[oid] = [output_data]

				
# This is saving the output data to an Excel sheet, you can change the location and name
excel_out = r"C:\temp\Nest_Neighbor_Data.xls"
wb = xlwt.Workbook()
ws = wb.add_sheet("Sheet1")
row = 0

for key, value in output.items():
	for nest in value:
		ws.write(row, 0, key)
		ws.write(row, 1, nest[0])
		ws.write(row, 2, nest[1])
		ws.write(row, 3, nest[2])
		ws.write(row, 4, nest[3])
		ws.write(row, 5, nest[4])
		ws.write(row, 6, nest[5])
		ws.write(row, 7, nest[6])
		ws.write(row, 8, nest[7])
		row += 1		
wb.save(excel_out)