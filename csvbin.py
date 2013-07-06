#!/usr/local/bin/python

""" 

Takes a csv of points and converts it to a shapefile,
running that through binify and coming out with a
hexbinned shapefile of the original points.

CSV to SHP script from http://pastebin.com/me0Zxqd6

More info on binify at https://github.com/kevinschaul/binify

"""

from osgeo import ogr, osr
from gdalconst import GA_ReadOnly
import csv, os
from subprocess import call

# Set the csv of points in lat/long format, 
# a intermediary shapefile of points
# and the final hexbinned shapefile
INPUT = "inpoints.csv"
POINTSHP = "outpoints.shp"
BINSHP = "outbin.shp"

driver = ogr.GetDriverByName('ESRI Shapefile')
 
def loadCSV(path=None):    
    global driver
    print("loading csv file %s" % path)
    fileReader = csv.reader(open(path), delimiter=',',)
  
    # check if shapefile exists and if so, delete it
    if os.path.exists(POINTSHP):
        driver.DeleteDataSource(POINTSHP)
    shape = driver.CreateDataSource(POINTSHP)
    
    # set projection of intermediary point shapefile to WGS84. Adjust as needed.
    proj = osr.SpatialReference()
    proj.SetWellKnownGeogCS( "EPSG:4326" )
    
    # create layer, setting the projection, then create the non-point fields
    header = fileReader.next()    
    layer = shape.CreateLayer('layerName',
                              geom_type=ogr.wkbPoint,
                              srs = proj)    
    layer.CreateField(ogr.FieldDefn("event",ogr.OFTString))
    
    # read lines in the csv and write info to shapefile
    for line in fileReader:
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("event",line[0])
        point = ogr.Geometry(ogr.wkbPoint)
        point.SetPoint_2D(0,float(line[7]),float(line[8]))
        feature.SetGeometry(point)
        layer.CreateFeature(feature)
        feature.Destroy()
        
loadCSV(INPUT)

# call binify. Check documentation for options
call("binify %s %s -e -o -n 32" % (POINTSHP, BINSHP))