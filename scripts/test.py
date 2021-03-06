"""
@summary: 
@author: CJ Grady
@version: 
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
from osgeo import ogr
import os

def featuresIntersect(geom1, geom2):
   return geom2.Intersects(geom1)

fn = "/home/cjgrady/workspace/occDataMiningPOC/data/layers/continent.shp"
ptWkt = "POINT (-70.85 -33.2667)"

ptFeature = ogr.CreateGeometryFromWkt(ptWkt)

print os.path.exists(fn)

conts = ogr.Open(fn)
lyr = conts.GetLayer()

for index in xrange(lyr.GetFeatureCount()):
   feature1 = lyr.GetFeature(index)
   print featuresIntersect(feature1.GetGeometryRef(), ptFeature)
