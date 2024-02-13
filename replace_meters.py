#Mary DuBose
#May 16, 2018
#Script to update the meter layer while maintaining the old geometries

import arcpy

oldMeters = r"Database Connections\pmlgw_bob.sde\PMLGW.DBO.MLGW_GSR_digitize\PMLGW.DBO.mlgw_gas_meter_rc_sj"
newMeters = r"S:\Data\MLGW\GSR\MaintenancePhase\UpdatedLayers\GasMetersV3.gdb\mlgw_meters_NEW"

matchedMeters = []
unmatchedMeters = {}
premisesOld = []
meterLocations = {}

#go through all meters in the current layer and store the geometry info in a dictionary where the premise number is the key
with arcpy.da.SearchCursor(oldMeters, ["PREMCODE", "SHAPE@XY", "last_edited_user", "last_edited_date"]) as cursor: 
	for row in cursor:
		prem = row[0]
		premisesOld.append(prem)
		meterLocations[prem] = [row[1], row[2], row[3]]

#go through all meters in the new layer and if the premise code matches with an existing meter, update the geometry to match the existing meter		
with arcpy.da.UpdateCursor(newMeters, ["PREM_CODE", "STREET_NUM", "DIR_PRE", "STREET_NAME", "SSFX", "PDIR_POST", "SHAPE@", "last_edited_user", "last_edited_date"]) as cursor2:
	for row in cursor2:
		prem = row[0]
		if prem in premisesOld:
			geom = meterLocations[prem][0]
			row[6] = geom
			row[7] = meterLocations[prem][1]
			row[8] = meterLocations[prem][2]
			cursor2.updateRow(row)
			matchedMeters.append(prem)
		else:
			unmatchedMeters[prem] = [row[1], row[2], row[3], row[4], row[5]] 
			
oldSet = set(premisesOld)
matchedSet = set(matchedMeters)
removedMeters = oldSet.difference(matchedSet)

file_r = r"S:\Tech\medubose\GSR_info\removed_meters.txt"
file_u = r"S:\Tech\medubose\GSR_info\unmatched_meters.txt"

with open(file_r, 'w') as writefile:
	for premcode in removedMeters:
		writefile.write("{}\n".format(premcode))
	
with open(file_u, 'w') as writefile:
	for key, value in unmatchedMeters.items():
		writefile.write("{0}: {1}\n".format(key, value))
