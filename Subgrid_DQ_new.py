#Mary DuBose
#July 19, 2021
#This script is to run the GSR subgrid definition query in ArcPro
#version: Python 3

import arcpy

img = "GSR Image"
sgc = "SG_cover"
sg= "Subgrids"

def main():
	aprx = arcpy.mp.ArcGISProject('CURRENT') # get current ArcPro project
	m = aprx.activeMap # get map from within project
	
	SID = arcpy.GetParameterAsText(0) # user needs to type in subgrid ID as parameter
	SID = SID.upper() # convert to uppercase in case user types in lowercase SID
	
	lyrs = m.listLayers() # access list of all layers in map
	sglyr = m.listLayers(sg)[0] # accessing the subgrid layer specifically
	
	for lyr in lyrs:

		if lyr.name == img:
			arcpy.AddMessage(SID) # prints subgrid name
			query = f"Score >= 85 AND SID = '{SID}' AND residential = 'Y'" # query can be modified to fit project needs
			lyr.definitionQuery = None # reset DQ
			
			lyr.definitionQuery = query	 # set the new DQ on GSR Image layer

		if lyr.name == sgc:
			query = f"""SID <> '{SID}'""" 
			lyr.definitionQuery = None
			lyr.definitionQuery = query # sets DQ to remove subgrid from subgrid cover layer
			query = f"""SID = '{SID}'""" # new query for actual subgrid layer (for panning to it)
			arcpy.management.SelectLayerByAttribute(sglyr,"NEW_SELECTION", query) # select the subgrid in order to pan to it
			mv = aprx.activeView # get active MapView of project
			mv.panToExtent(mv.getLayerExtent(sglyr, True)) # get extent of selected subgrid and pan to it
			arcpy.SelectLayerByAttribute_management(sglyr, "CLEAR_SELECTION") # deselect the subgrid


if __name__ == '__main__':
	main()
