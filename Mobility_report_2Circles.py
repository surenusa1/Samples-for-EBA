#This python file will generate the area coverage report for a state intersecting with nearby 2 states.
#This will generate a local workspace and generate the required report

import os
import arcpy
from arcpy import env
from arcpy.sa import *
import shutil
import time
import fnmatch
# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True
#local workspace and variables used in the current file
BASECIRCLENAME=arcpy.GetParameterAsText(0)
CIRCLENAME1=arcpy.GetParameterAsText(1)

INPUTDATALOCATION="Z:\SPO Data\Aug_Mobility\INPUT\NE_INPUT"
OUTPUTLOCATION="Z:\SPO Data\Aug_Mobility\OUTPUT\NE_OUTPUT"
#DEFAULTWORKSPACE="D:\\Airtel\\ModelOutput"
BASECIRCLELOCATION=INPUTDATALOCATION+"\\"+BASECIRCLENAME
DEFAULTWORKSPACE=OUTPUTLOCATION
CIRCLE1LOCATION=INPUTDATALOCATION+"\\"+CIRCLENAME1

#Input Files of base circle
BASEGRDFILENAME=[f for f in os.listdir(BASECIRCLELOCATION) if f.endswith('.grd')]
BASECIRCLEGRD=BASECIRCLELOCATION+"\\"+BASEGRDFILENAME[0]+"\\Band_4"
BASECIRCLESHPNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*district*.shp')]
BASECIRCLESHP=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPNAME[0]
BASECIRCLESHPVILLNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*village*.shp')]
BASECIRCLESHPVILL=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPVILLNAME[0]
BASECIRCLESHPTOWNNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*town*.shp')]
BASECIRCLESHPTOWN=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPTOWNNAME[0]
BASECIRCLEGRCNAME=[f for f in os.listdir(BASECIRCLELOCATION) if f.endswith('.img')]
BASECIRCLEGRC=BASECIRCLELOCATION+"\\"+BASECIRCLEGRCNAME[0]
BASECIRCLEGRCTIFF=BASECIRCLELOCATION+"\\"+BASECIRCLENAME+"_grcTiff.tif"

#creating tiff file form img file for circle1
arcpy.CompositeBands_management(BASECIRCLEGRC, BASECIRCLEGRCTIFF)

#GRD file location for circle1
CIRCLENAME1LOC=INPUTDATALOCATION+"\\"+CIRCLENAME1
GRDFILENAME1=[f for f in os.listdir(CIRCLENAME1LOC) if f.endswith('.grd')]
CIRCLEGRD1=CIRCLENAME1LOC+"\\"+GRDFILENAME1[0]+"\\Band_4"
CIRCLE1GRCNAME=[f for f in os.listdir(CIRCLE1LOCATION) if f.endswith('.img')]
CIRCLE1GRC=CIRCLE1LOCATION+"\\"+CIRCLE1GRCNAME[0]
CIRCLE1GRCTIFF=CIRCLE1LOCATION+"\\"+CIRCLENAME1+"_grcTiff.tif"
#creating tiff file form img file for circle1
arcpy.CompositeBands_management(CIRCLE1GRC, CIRCLE1GRCTIFF)
#****************************************************************#
#######Input file location for circle1 ends here


#create a fileGDB for processing

if os.path.exists(DEFAULTWORKSPACE):
    #os.rmdir(DEFAULTWORKSPACE+"\\"+BASECIRCLENAME+".gdb")
    shutil.rmtree(DEFAULTWORKSPACE)
os.makedirs(DEFAULTWORKSPACE)
print "Directory Created"

POSTGRESDBPATH = r"C:\Users\Administrator\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\mobility.sde"
#Create Default workspace where calculation is performed to generate reports
arcpy.CreateFileGDB_management(DEFAULTWORKSPACE,BASECIRCLENAME+".gdb")

#Default workspace
DEFAULTWORKSPACENAME=DEFAULTWORKSPACE+"\\"+BASECIRCLENAME+".gdb"

#Intermediate Output during report generationn
BASECIRCLEGRDTIFF=DEFAULTWORKSPACE+"\\basecirclegrd.tif"
RECLASSIFY_OUTPUT=DEFAULTWORKSPACENAME+"\\reclassify_raster"
BUFFER_OUTPUT=DEFAULTWORKSPACENAME+"\\buffer_output"
EXTRACTBYMASK_OUTPUT=DEFAULTWORKSPACE+"\\out_EBM"
RASTER2POLY_OUTPUT=DEFAULTWORKSPACENAME+"\\raster2poly"
DISSOLVE_OUTPUT=DEFAULTWORKSPACENAME+"\\dissolve_output"
CLIP_OUTPUT=DEFAULTWORKSPACENAME+"\\clipoutput"
UNION_OUTPUT=DEFAULTWORKSPACENAME+"\\union_polygon_output"
AREA_OUTPUT=DEFAULTWORKSPACENAME+"\\polygon_output"
COPY_OUTPUT=POSTGRESDBPATH+"\\NE_Area"
POINT_OUTPUT = POSTGRESDBPATH+"\\NE_point"
MAKE_QUERY_OUTPUT=DEFAULTWORKSPACENAME+"\\make_query_table"
EXCEL_OUTPUT=DEFAULTWORKSPACE+"\\area_coverage.xls"
NH_OUTPUT=DEFAULTWORKSPACE+"\\NH_output.shp"
SH_OUTPUT=DEFAULTWORKSPACE+"\\SH_output.shp"
MR_OUTPUT=DEFAULTWORKSPACE+"\\MR_output.shp"
MM_OUTPUT=DEFAULTWORKSPACE+"\\MM_output.shp"
RAIL_OUTPUT=DEFAULTWORKSPACE+"\\RAIL_output.shp"
OTHERROAD_OUTPUT=DEFAULTWORKSPACE+"\\OTHERROAD_output.shp"
othertownlayer = DEFAULTWORKSPACE+"\\othertown.shp"
emptytownlayer= DEFAULTWORKSPACE+"\\EMPtown.shp"
BESETTOWN_SELECT_OUTPUT=DEFAULTWORKSPACENAME+"\\townSelect_output"
#BESTTOWN_OUTPUT="bestTown_out.dbf"
EMPTYPOINT_OUT = DEFAULTWORKSPACE+"\\HPEMPTY.dbf"
EMPTYPOINT="HPEMPTY"
BESTTOWN_OUT = DEFAULTWORKSPACE+"\\bestTown.dbf"
BESTTOWN_OUTPUT="bestTown"
OTHERTOWN_OUT = DEFAULTWORKSPACE +"\\othTown.dbf"
OTHERTOWN_OUTPUT="othTown"
EMPTYTOWN_OUT = DEFAULTWORKSPACE +"\\emptyTown.dbf"
EMPTYTOWN_OUTPUT="emptyTown"
OTHTOWN_SELECT_OUTPUT=DEFAULTWORKSPACENAME+"\\othTownSelect_output"
#OTHTTOWN_INTER_OUTPUT=DEFAULTWORKSPACENAME+"\\othTownIntersect_output"
#OTHERTOWN_OUTPUT="othTown_out.dbf"
EMPTYTOWN_SELECT_OUTPUT=DEFAULTWORKSPACENAME+"\\emptyTownSelect_output"
#EMPTYTOWN_INTER_OUTPUT=DEFAULTWORKSPACENAME+"\\emptyTownIntersect_output"
#EMPTYTOWN_OUTPUT="emptyTown_out.dbf"

print BASECIRCLEGRD
print BASECIRCLEGRDTIFF

# Process: Composite Bands
if os.path.exists(BASECIRCLEGRDTIFF):
    os.remove(BASECIRCLEGRDTIFF)

arcpy.CompositeBands_management(BASECIRCLEGRD, BASECIRCLEGRDTIFF)
#arcpy.CopyRaster_management(BASECIRCLEGRD, BASECIRCLEGRDTIFF, "", "", "-1.000000e+037", "NONE", "NONE", "", "NONE", "NONE")
print "Copy Raster Executed"
print arcpy.GetMessages()

# Process: Mosaic
arcpy.Mosaic_management([CIRCLEGRD1], BASECIRCLEGRDTIFF, "MAXIMUM", "FIRST", "", "", "NONE", "0", "NONE")
print "Mosaic Executed"
print arcpy.GetMessages()

# Process: Reclassify
arcpy.gp.Reclassify_sa(BASECIRCLEGRDTIFF,"Value","-1000 -93 5;-93 -85 4;-85 -75 3;-75 -65 2;-65 0 1",RECLASSIFY_OUTPUT,"DATA")
print "Reclassify Executed"
print arcpy.GetMessages()

#Process: Buffer
arcpy.Buffer_analysis(in_features=BASECIRCLESHP,out_feature_class=BUFFER_OUTPUT,buffer_distance_or_field="1 Kilometers",line_side="FULL",line_end_type="ROUND",dissolve_option="ALL",dissolve_field="#")
print "Buffer"
print arcpy.GetMessages()

#Process: Extract By Mask
arcpy.gp.ExtractByRectangle_sa(RECLASSIFY_OUTPUT,BUFFER_OUTPUT,EXTRACTBYMASK_OUTPUT,"INSIDE")
print "ExtractByRectangle"
print arcpy.GetMessages()

# Process: Raster to Polygon
print RECLASSIFY_OUTPUT
print RASTER2POLY_OUTPUT
arcpy.RasterToPolygon_conversion(EXTRACTBYMASK_OUTPUT, RASTER2POLY_OUTPUT, "NO_SIMPLIFY", "Value")
print "Raster to Polygon Executed"
print arcpy.GetMessages()

# Process: Clip
arcpy.Clip_analysis(RASTER2POLY_OUTPUT, BASECIRCLESHP, CLIP_OUTPUT)
print "Clip Executed"
print arcpy.GetMessages()

# Process: Union
arcpy.Union_analysis([BASECIRCLESHP,CLIP_OUTPUT], UNION_OUTPUT, "ALL", "", "GAPS")
print "Union Executed"
print arcpy.GetMessages()

# Process: Add Geometry Attribute Data Management
arcpy.AddGeometryAttributes_management(Input_Features=UNION_OUTPUT, Geometry_Properties="AREA;AREA_GEODESIC", Length_Unit="KILOMETERS", Area_Unit="SQUARE_KILOMETERS", Coordinate_System="")
print "Area Calculation Executed"
# Process: Calculate Areas
#arcpy.CalculateAreas_stats(UNION_OUTPUT, AREA_OUTPUT)
#print "Calculate Areas Executed"

#generating report for area coverage
# Process: Copy rows
# The tool will prepares the input table which can be then stored on the Dbase or ArcSDE table.
arcpy.CopyRows_management(UNION_OUTPUT,COPY_OUTPUT)
print "Copy Rows Executed"


#generating report for area coverage ends here 
#************************************************************************#

#generating report for NH
#NH input
BASECIRCLESHPNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*NH*.shp')]
BASECIRCLE_NH_SHP=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPNAME[0]

arcpy.Intersect_analysis(in_features=[UNION_OUTPUT,BASECIRCLE_NH_SHP], out_feature_class=NH_OUTPUT, join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="LINE")

NH_FIELD="NH_Length"
arcpy.AddField_management(in_table=NH_OUTPUT, field_name=NH_FIELD, field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=NH_OUTPUT, field=NH_FIELD, expression="!shape.length@kilometers!", expression_type="PYTHON_9.3", code_block="")
print "NH Calculated"

arcpy.TableToTable_conversion(in_rows=NH_OUTPUT, out_path=POSTGRESDBPATH, out_name="NE_NH", where_clause="", field_mapping="", config_keyword="")
print "NH Result generated"
#NH_table is generated
#generating report for NH ends here
#************************************************************************#

#generating report for SH
#SH input
BASECIRCLESHPNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*SH*.shp')]
BASECIRCLE_SH_SHP=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPNAME[0]

arcpy.Intersect_analysis(in_features=[UNION_OUTPUT,BASECIRCLE_SH_SHP], out_feature_class=SH_OUTPUT, join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="LINE")

SH_FIELD="SH_Length"
arcpy.AddField_management(in_table=SH_OUTPUT, field_name=SH_FIELD, field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=SH_OUTPUT, field=SH_FIELD, expression="!shape.length@kilometers!", expression_type="PYTHON_9.3", code_block="")
print "SH Calculated"

arcpy.TableToTable_conversion(in_rows=SH_OUTPUT, out_path=POSTGRESDBPATH, out_name="NE_SH", where_clause="", field_mapping="", config_keyword="")
print "SH Result generated"
#SH_table is generated
#generating report for SH ends here
#************************************************************************#

#generating report for MR
#MR input
BASECIRCLESHPNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*MR*.shp')]
BASECIRCLE_MR_SHP=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPNAME[0]

arcpy.Intersect_analysis(in_features=[UNION_OUTPUT,BASECIRCLE_MR_SHP], out_feature_class=MR_OUTPUT, join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="LINE")

MR_FIELD="MR_Length"
arcpy.AddField_management(in_table=MR_OUTPUT, field_name=MR_FIELD, field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=MR_OUTPUT, field=MR_FIELD, expression="!shape.length@kilometers!", expression_type="PYTHON_9.3", code_block="")
print "MR Calculated"

arcpy.TableToTable_conversion(in_rows=MR_OUTPUT, out_path=POSTGRESDBPATH, out_name="NE_MR", where_clause="", field_mapping="", config_keyword="")
print "MR Result generated"
#MR_table is generated
#generating report for MR ends here
#************************************************************************#

#generating report for MM
#MM input
BASECIRCLESHPNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*MM*.shp')]
BASECIRCLE_MM_SHP=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPNAME[0]

arcpy.Intersect_analysis(in_features=[UNION_OUTPUT,BASECIRCLE_MM_SHP], out_feature_class=MM_OUTPUT, join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="LINE")

MM_FIELD="MM_Length"
arcpy.AddField_management(in_table=MM_OUTPUT, field_name=MM_FIELD, field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=MM_OUTPUT, field=MM_FIELD, expression="!shape.length@kilometers!", expression_type="PYTHON_9.3", code_block="")
print "MM Calculated"

arcpy.TableToTable_conversion(in_rows=MM_OUTPUT, out_path=POSTGRESDBPATH, out_name="NE_MM", where_clause="", field_mapping="", config_keyword="")
print "MM Result generated"
#MM_table is generated
#generating report for MM ends here

#************************************************************************#
#generating report for RAIL
#RAIL input
BASECIRCLESHPNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*RAIL*.shp')]
BASECIRCLE_RAIL_SHP=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPNAME[0]

arcpy.Intersect_analysis(in_features=[UNION_OUTPUT,BASECIRCLE_RAIL_SHP], out_feature_class=RAIL_OUTPUT, join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="LINE")

RAIL_FIELD="Length"
arcpy.AddField_management(in_table=RAIL_OUTPUT, field_name=RAIL_FIELD, field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=RAIL_OUTPUT, field=RAIL_FIELD, expression="!shape.length@kilometers!", expression_type="PYTHON_9.3", code_block="")
print "RAIL Calculated"

arcpy.TableToTable_conversion(in_rows=RAIL_OUTPUT, out_path=POSTGRESDBPATH, out_name="NE_RAIL", where_clause="", field_mapping="", config_keyword="")
print "RAIL Result generated"
#RAIL_table is generated
#generating report for RAIL ends here
#************************************************************************#

#generating report for OTHERROADS
#OTHERROADS input
BASECIRCLESHPNAME=[f for f in os.listdir(BASECIRCLELOCATION+"\\Vector") if fnmatch.fnmatch(f,'*OTHERROADS*.shp')]
BASECIRCLE_OTHERROAD_SHP=BASECIRCLELOCATION+"\\Vector\\"+BASECIRCLESHPNAME[0]

arcpy.Intersect_analysis(in_features=[UNION_OUTPUT,BASECIRCLE_OTHERROAD_SHP], out_feature_class=OTHERROAD_OUTPUT, join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="LINE")

OR_FIELD="Length"
arcpy.AddField_management(in_table=OTHERROAD_OUTPUT, field_name=OR_FIELD, field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=OTHERROAD_OUTPUT, field=OR_FIELD, expression="!shape.length@kilometers!", expression_type="PYTHON_9.3", code_block="")
print "OTHERROADS Calculated"

arcpy.TableToTable_conversion(in_rows=OTHERROAD_OUTPUT, out_path=POSTGRESDBPATH, out_name="NE_OTHERROAD", where_clause="", field_mapping="", config_keyword="")
print "Other Roads Result generated"
#OTHERROAD_table is generated
#generating report for OTHERROAD ends here
#************************************************************************#




#************************************************************************#
###### VillageCoverage starts here
#************************************************************************#
#Execute Feature to point as the input point data contains multipoint
BASECIRCLE_POINTS=DEFAULTWORKSPACE+"\\FeatureToPoint_Output.shp"
arcpy.FeatureToPoint_management(in_features=BASECIRCLESHPVILL,out_feature_class=BASECIRCLE_POINTS,point_location="CENTROID")

#Execute Values to point for baseclass grd values
BASECIRCLE_GRD_OUT=DEFAULTWORKSPACENAME+"\\basecir_grdadd"
BASECIRCLE_GRC_OUT=DEFAULTWORKSPACENAME+"\\basecir_grcadd"

#arcpy.ExtractValuesToPoints (in_point_features=BASECIRCLE_POINTS, in_raster=BASECIRCLEGRD, out_point_features=BASECIRCLE_GRD_OUT, "NONE", "VALUE_ONLY")
arcpy.gp.ExtractValuesToPoints_sa(BASECIRCLE_POINTS,BASECIRCLEGRD,BASECIRCLE_GRD_OUT,"NONE","VALUE_ONLY")
arcpy.AlterField_management(in_table=BASECIRCLE_GRD_OUT,field="RASTERVALU",new_field_name=BASECIRCLENAME+"_SS",new_field_alias=BASECIRCLENAME+"_SS")

#Execute Values to point for base class grc values

#arcpy.ExtractValuesToPoints (in_point_features=BASECIRCLE_GRD_OUT, in_raster=BASECIRCLEGRCTIFF, out_point_features=BASECIRCLE_GRC_OUT, "NONE", "VALUE_ONLY")
arcpy.gp.ExtractValuesToPoints_sa(BASECIRCLE_GRD_OUT,BASECIRCLEGRCTIFF,BASECIRCLE_GRC_OUT,"NONE","VALUE_ONLY")
arcpy.AlterField_management(in_table=BASECIRCLE_GRC_OUT,field="RASTERVALU",new_field_name=BASECIRCLENAME+"_SID",new_field_alias=BASECIRCLENAME+"_SID")
print "Data collected for "+BASECIRCLENAME
# grd grc for basecircle ends here
#****************************************************************************************

#Execute Values to point for Intersecting circle1 grd values
CIRCLE1_GRD_OUT=DEFAULTWORKSPACENAME+"\\circle1_grdadd"
CIRCLE1_GRC_OUT=DEFAULTWORKSPACENAME+"\\circle1_grcadd"

#arcpy.ExtractValuesToPoints (in_point_features=BASECIRCLE_GRC_OUT, in_raster=CIRCLE1GRD, out_point_features=CIRCLE1_GRD_OUT, "NONE", "VALUE_ONLY")
arcpy.gp.ExtractValuesToPoints_sa(BASECIRCLE_GRC_OUT,CIRCLEGRD1,CIRCLE1_GRD_OUT,"NONE","VALUE_ONLY")
arcpy.AlterField_management(in_table=CIRCLE1_GRD_OUT,field="RASTERVALU",new_field_name=CIRCLENAME1+"_SS",new_field_alias=CIRCLENAME1+"_SS")

#Execute Values to point for Intersecting circle1 grc values

#arcpy.ExtractValuesToPoints (in_point_features=CIRCLE1_GRD_OUT, in_raster=CIRCLE1GRCTIFF, out_point_features=CIRCLE1_GRC_OUT, "NONE", "VALUE_ONLY")
arcpy.gp.ExtractValuesToPoints_sa(CIRCLE1_GRD_OUT,CIRCLE1GRCTIFF,CIRCLE1_GRC_OUT,"NONE","VALUE_ONLY")
arcpy.AlterField_management(in_table=CIRCLE1_GRC_OUT,field="RASTERVALU",new_field_name=CIRCLENAME1+"_SID",new_field_alias=CIRCLENAME1+"_SID")
print "Data collected for "+CIRCLENAME1
# grd grc for CIRCLE1 ends here
#****************************************************************************************

#Select the rows which for Best village coverage
BEST_BASECIRCLE=DEFAULTWORKSPACENAME+"\\"+BASECIRCLENAME+"_Best"
arcpy.TableSelect_analysis(in_table=CIRCLE1_GRC_OUT,out_table=BEST_BASECIRCLE,where_clause=BASECIRCLENAME+"_SS > "+CIRCLENAME1+"_SS")
#DROP FIELDS
BASECIRCLEDropFields = [CIRCLENAME1+"_SS", CIRCLENAME1+"_SID"]
  
# Execute DeleteField
arcpy.DeleteField_management(BEST_BASECIRCLE, BASECIRCLEDropFields)
# Add Coverage_Circle field
arcpy.AddField_management(in_table=BEST_BASECIRCLE, field_name="CvgCircle", field_type="TEXT", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
# calculate CvgCircle field
arcpy.CalculateField_management(BEST_BASECIRCLE, "CvgCircle", "\"NE\"", "PYTHON_9.3")
#Make Table View
arcpy.MakeTableView_management(in_table=CIRCLE1_GRC_OUT,out_view="circle2_grcadd_View1")
#Select layer by attribute management to select the records and delete from the input table
arcpy.SelectLayerByAttribute_management("circle2_grcadd_View1", "NEW_SELECTION", BASECIRCLENAME+"_SS > "+CIRCLENAME1+"_SS")
#Delete rows from the table
arcpy.DeleteRows_management("circle2_grcadd_View1")

#Circle 1
BEST_CIRCLE1=DEFAULTWORKSPACENAME+"\\"+CIRCLENAME1+"_Best"
arcpy.TableSelect_analysis(in_table=CIRCLE1_GRC_OUT,out_table=BEST_CIRCLE1,where_clause=CIRCLENAME1+"_SS > "+BASECIRCLENAME+"_SS")
#DROP FIELDS
BASECIRCLEDropFields = [BASECIRCLENAME+"_SS", BASECIRCLENAME+"_SID"]
  
# Execute DeleteField
arcpy.DeleteField_management(BEST_CIRCLE1, BASECIRCLEDropFields)

#alter field
arcpy.AlterField_management(BEST_CIRCLE1,field=CIRCLENAME1+"_SID",new_field_name=BASECIRCLENAME+"_SID",new_field_alias=BASECIRCLENAME+"_SID")
arcpy.AlterField_management(BEST_CIRCLE1,field=CIRCLENAME1+"_SS",new_field_name=BASECIRCLENAME+"_SS",new_field_alias=BASECIRCLENAME+"_SS")
#Make Table View
# Add CvgCircle field
arcpy.AddField_management(in_table=BEST_CIRCLE1, field_name="CvgCircle", field_type="TEXT", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
# calculate CvgCircle field
arcpy.CalculateField_management(BEST_CIRCLE1, "CvgCircle", "\"AS\"", "PYTHON_9.3")
#Make Table View
arcpy.MakeTableView_management(in_table=CIRCLE1_GRC_OUT,out_view="circle2_grcadd_View2")
#Select layer by attribute management to select the records and delete from the input table
arcpy.SelectLayerByAttribute_management("circle2_grcadd_View2", "NEW_SELECTION", CIRCLENAME1+"_SS > "+BASECIRCLENAME+"_SS")
#Delete rows from the table
arcpy.DeleteRows_management("circle2_grcadd_View2")

#empty village list generated
arcpy.TableToTable_conversion(in_rows=CIRCLE1_GRC_OUT,out_path=DEFAULTWORKSPACE,out_name=EMPTYPOINT)
#DROP FIELDS
BASECIRCLEDropFields = [CIRCLENAME1+"_SS", CIRCLENAME1+"_SID"]
  
# Execute DeleteField
arcpy.DeleteField_management(EMPTYPOINT_OUT, BASECIRCLEDropFields)
#Report files are
#Best_baseCircle_village.dbf - best of base circle
#Best_CircleName1_village.dbf - best of circle1
#Best_CircleName2_village.dbf - best of circle2
#Empty_Village.dbf - empty village list

#************************************************************************#
###### VillageCoverage ends here
#************************************************************************#
print "VillageCoverage Genarated"



#************************************************************************#
###### Town Report starts here
#************************************************************************#
#adding a field for calculation for town based result

TOWNFIELD="townFld"
arcpy.AddField_management(in_table=UNION_OUTPUT,field_name=TOWNFIELD,field_type="LONG",field_precision="#",field_scale="#",field_length="#",field_alias="#",field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="#")

#calculating field management
updateCursor = arcpy.UpdateCursor(UNION_OUTPUT)
for cursor in updateCursor:
    gridCodeVal = cursor.getValue("gridcode")
    if (gridCodeVal ==1 or gridCodeVal == 2 or gridCodeVal == 3):
        cursor.setValue("townFld",1)
    elif (gridCodeVal ==4):
        cursor.setValue("townFld",2)
    elif (gridCodeVal == 5):
        cursor.setValue("townFld",3)
    updateCursor.updateRow(cursor)

#selecting the records which are covered upto signal -85
arcpy.Select_analysis(in_features=UNION_OUTPUT,out_feature_class=BESETTOWN_SELECT_OUTPUT,where_clause=TOWNFIELD+" = 1")

#Make Feature Layer
arcpy.MakeFeatureLayer_management(BASECIRCLESHPTOWN,"BaseTown_Lyr")

#select by location
arcpy.SelectLayerByLocation_management(in_layer="BaseTown_Lyr",overlap_type="INTERSECT",select_features=BESETTOWN_SELECT_OUTPUT,search_distance="#",selection_type="NEW_SELECTION")
arcpy.TableToTable_conversion(in_rows="BaseTown_Lyr",out_path=DEFAULTWORKSPACE,out_name=BESTTOWN_OUTPUT,where_clause="#",field_mapping="#",config_keyword="#")
#Add Signal strength field
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "bestTown_out"
arcpy.AddField_management(in_table=BESTTOWN_OUT, field_name="NE_SS", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
# Add Signal strength Value
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "bestTown_out"
arcpy.CalculateField_management(in_table=BESTTOWN_OUT, field="NE_SS", expression="Reclass(!NE_SS!)", expression_type="PYTHON", code_block="def Reclass(NE_SS):\n  if (NE_SS == 0):\n   return -85\n")
# switch BaseTown_Lyr
arcpy.SelectLayerByAttribute_management("BaseTown_Lyr","SWITCH_SELECTION")

arcpy.CopyFeatures_management("BaseTown_Lyr",othertownlayer)

#arcpy.MakeFeatureLayer_management(in_layer="BaseTown_Lyr","otherTown_Lyr")
print "town test success"
#stored the records in .dbf file



#selecting the records which are covered upto signal -95
arcpy.Select_analysis(in_features=UNION_OUTPUT,out_feature_class=OTHTOWN_SELECT_OUTPUT,where_clause=TOWNFIELD+" = 2")

#Make Feature Layer
arcpy.MakeFeatureLayer_management(othertownlayer,"BestOtherTownSelect_Lyr")


#select by location
arcpy.SelectLayerByLocation_management(in_layer="BestOtherTownSelect_Lyr",overlap_type="INTERSECT",select_features=OTHTOWN_SELECT_OUTPUT,search_distance="#",selection_type="NEW_SELECTION")

#stored the records in .dbf file
arcpy.TableToTable_conversion(in_rows="BestOtherTownSelect_Lyr",out_path=DEFAULTWORKSPACE,out_name=OTHERTOWN_OUTPUT,where_clause="#",field_mapping="#",config_keyword="#")

#Add Signal strength field
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "bestTown_out"
arcpy.AddField_management(in_table=OTHERTOWN_OUT, field_name="NE_SS", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
# Add Signal strength Value
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "bestTown_out"
arcpy.CalculateField_management(in_table=OTHERTOWN_OUT, field="NE_SS", expression="Reclass(!NE_SS!)", expression_type="PYTHON", code_block="def Reclass(NE_SS):\n  if (NE_SS == 0):\n   return -93\n")
# switch otherTown_Lyr
arcpy.SelectLayerByAttribute_management("BestOtherTownSelect_Lyr","SWITCH_SELECTION")

arcpy.CopyFeatures_management("BestOtherTownSelect_Lyr",emptytownlayer)

#arcpy.MakeFeatureLayer_management(in_layer="BaseTown_Lyr","otherTown_Lyr")
print "OTHER town test success"
#stored the records in .dbf file
#selecting the records which are covered more than signal -95
arcpy.Select_analysis(in_features=UNION_OUTPUT,out_feature_class=EMPTYTOWN_SELECT_OUTPUT,where_clause=TOWNFIELD+" = 3")

#Make Feature Layer
arcpy.MakeFeatureLayer_management(emptytownlayer,"emptyTownSelect_Lyr")


#select by location
arcpy.SelectLayerByLocation_management(in_layer="emptyTownSelect_Lyr",overlap_type="INTERSECT",select_features=EMPTYTOWN_SELECT_OUTPUT,search_distance="#",selection_type="NEW_SELECTION")

#stored the records in .dbf file
arcpy.TableToTable_conversion(in_rows="emptyTownSelect_Lyr",out_path=DEFAULTWORKSPACE,out_name=EMPTYTOWN_OUTPUT,where_clause="#",field_mapping="#",config_keyword="#")


arcpy.AddField_management(in_table=EMPTYTOWN_OUT, field_name="NE_SS", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")#Report files are
# Merge all point tables

arcpy.Merge_management([BEST_BASECIRCLE,BEST_CIRCLE1,EMPTYPOINT_OUT,BESTTOWN_OUT,OTHERTOWN_OUT,EMPTYTOWN_OUT],POINT_OUTPUT)
#Report files are
#************************************************************************#
print "Town Output Generated"
print "Final Output Generated"
