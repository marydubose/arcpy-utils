# Mary DuBose
# October 18, 2023
# This script performs a daily check of the address point feature class.
# It compares the features to a backup copy to check for added or deleted points.

import arcpy
import os
from optparse import OptionParser
import sys
sys.path.append(r"C:\{}\projects\py-caeser".format(os.environ['USERNAME'].lower()))
import cpgis

email_text = ""

usage = "usage: %prog [options] arg"
op = OptionParser(usage)
op.add_option("-u", "--user", dest="user")
op.add_option("-p", "--password", dest="password")
(options, args) = op.parse_args()
	
version = u'"UOM\\MEDUBOSE".medubose'
sde_connection = r"C:\temp\PDPD_medubose_qc.sde"
cpgis.dbConnect("PCOM", options.user, options.password, "PDPD", version,
					 sde_connection)

pcom_version = sde_connection + r"\PDPD.DBO.DPD_Signs\PDPD.DBO.AddressPoints"
bu_version = r"S:\Admin\backups\pcom\DPD_Signs_Backup.gdb\AddressPoints_bu"

pcom_list = []
bu_list = []
null_list = []

with arcpy.da.SearchCursor(pcom_version, ("OBJECTID", "OIRID")) as cur:
	for row in cur:
		if row[1] is None or row[1] == "":
			null_list.append(str(row[0]))
		else:
			pcom_list.append(str(row[1]))
			
with arcpy.da.SearchCursor(bu_version, ("OBJECTID", "OIRID")) as cur2:
	for row in cur2:
		bu_list.append(str(row[1]))
		
for oirid in pcom_list:
	if oirid not in bu_list:
		email_text += f"Address Point {oirid} does not appear in backup data. Check and possibly delete.\n"
		
for oirid in bu_list:
	if oirid not in pcom_list:
		email_text += f"Address Point {oirid} is in the backup but not in PCOM. Possibly deleted!!!\n"
		
for objid in null_list:
	email_text += f"Address point with objectid {objid} has a null identifier. Check this one.\n"

if email_text != "":
	recipients = ["medubose@memphis.edu"]
	subject = "DPD Signs Address Points - Changes Detected"
	cpgis.sendEmail(recipients, subject, email_text)