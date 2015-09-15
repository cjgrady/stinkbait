"""
@summary: Module containing methods to rewrite CSV files
@author: CJ Grady
@version: 1.0
@status: alpha

@license: gpl2
@copyright: Copyright (C) 2014, University of Kansas Center for Research

          Lifemapper Project, lifemapper [at] ku [dot] edu, 
          Biodiversity Institute,
          1345 Jayhawk Boulevard, Lawrence, Kansas, 66045, USA
   
          This program is free software; you can redistribute it and/or modify 
          it under the terms of the GNU General Public License as published by 
          the Free Software Foundation; either version 2 of the License, or (at 
          your option) any later version.
  
          This program is distributed in the hope that it will be useful, but 
          WITHOUT ANY WARRANTY; without even the implied warranty of 
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
          General Public License for more details.
  
          You should have received a copy of the GNU General Public License 
          along with this program; if not, write to the Free Software 
          Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
          02110-1301, USA.
"""
import csv
import os
from osgeo import ogr

from dataHelpers.regions import CONTINENTS_LOOKUP, COUNTRIES_LOOKUP, STATES_LOOKUP

LAYERS_DIR = "/home/cjgrady/workspace/occDataMiningPOC/data/layers/"

CONTINENTS_FN = os.path.join(LAYERS_DIR, "continent.shp")
COUNTRIES_FN = os.path.join(LAYERS_DIR, "WorldCountries2011.shp")
STATES_FN = os.path.join(LAYERS_DIR, "states_dd.shp")

CONTINENT_FIELD = "CONTINENT"
COUNTRY_FIELD = "COUNTRY"
STATE_FIELD = "STATE_NAME"

IN_DIR = "/home/cjgrady/workspace/occDataMiningPOC/data/modCSVs"
OUT_DIR = "/home/cjgrady/workspace/occDataMiningPOC/data/finalCsvs"


def getIntersectedContinent(ptGeom):
   continents = ogr.Open(CONTINENTS_FN)
   lyr = continents.GetLayer()
   ret = -1
   for index in xrange(lyr.GetFeatureCount()):
      feat = lyr.GetFeature(index)
      ftGeom = feat.GetGeometryRef()
      if ptGeom.Intersects(ftGeom):
         ret = CONTINENTS_LOOKUP[feat.GetField(CONTINENT_FIELD).lower()]
   lyr = None
   states = None
   return ret

def getIntersectedCountry(ptGeom):
   countries = ogr.Open(COUNTRIES_FN)
   lyr = countries.GetLayer()
   ret = -1
   for index in xrange(lyr.GetFeatureCount()):
      feat = lyr.GetFeature(index)
      ftGeom = feat.GetGeometryRef()
      if ptGeom.Intersects(ftGeom):
         ret = COUNTRIES_LOOKUP[feat.GetField(COUNTRY_FIELD).lower()]
   lyr = None
   states = None
   return ret

def getIntersectedState(ptGeom):
   states = ogr.Open(STATES_FN)
   lyr = states.GetLayer()
   ret = -1
   for index in xrange(lyr.GetFeatureCount()):
      feat = lyr.GetFeature(index)
      ftGeom = feat.GetGeometryRef()
      if ptGeom.Intersects(ftGeom):
         ret = STATES_LOOKUP[feat.GetField(STATE_FIELD).lower()]
   lyr = None
   states = None
   return ret

def rewriteCsvFile(inPtsFn, outPtsFn):
   """
   @summary: Rewrites points in format: provider, continent, country, state
   """
   with open(inPtsFn) as inF:
      reader = csv.reader(inF)
         
      headers = reader.next()
         
      with open(outPtsFn, 'w') as outF:
         writer = csv.writer(outF)
         writer.writerow(["provider", "continent", "country", "state"])
         
         rIdx = 0
         for row in reader:
            rIdx += 1
            print "   row -", rIdx
            lat, lon, provider = row
            
            ptWkt = "POINT (%s %s)" % (lon, lat)
            ptGeom = ogr.CreateGeometryFromWkt(ptWkt)
            
            writer.writerow([provider, 
                             getIntersectedContinent(ptGeom), 
                             getIntersectedCountry(ptGeom), 
                             getIntersectedState(ptGeom)])
   
# .............................................................................   
def rewriteCsvForName(rawName):
   name = rawName.replace(' ', '_')
   try:
      csvFn = "%s.csv" % name
      inFn = os.path.join(IN_DIR, csvFn)
      outFn = os.path.join(OUT_DIR, csvFn)
      rewriteCsvFile(inFn, outFn)
   except Exception, e:
      print str(e)

# .............................................................................   
if __name__ == "__main__":
   import sys
   
   if len(sys.argv) > 1:
      tName = sys.argv[1]
      rewriteCsvForName(tName)
   else:
      namesFn = "/home/cjgrady/workspace/occDataMiningPOC/data/other/taxaNames.txt"
   
      with open(namesFn) as namesF:
         for line in namesF:
            name = line.strip().replace(' ', '_')
            print name
            rewriteCsvForName(name)
         
