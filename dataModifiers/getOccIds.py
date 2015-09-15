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
import os
import urllib2

inNamesFn = "/home/cjgrady/workspace/occDataMiningPOC/data/other/taxaNames.txt"
outNamesFn = "/home/cjgrady/workspace/occDataMiningPOC/data/other/taxaNamesWithIds.txt"
outDir = "/home/cjgrady/workspace/occDataMiningPOC/data/csvs/"

def getOccIdForName(name):
   url = "http://lifemapper.org/hint/species/%s" % name.replace(' ', '%20')
   lines = urllib2.urlopen(url).readlines()
   for line in lines:
      parts = line.split('\t')
      if parts[0].strip() == name:
         return parts[1].strip()
   return None

def getCsv(occId, fn):
   url = "http://lifemapper.org/services/occurrences/%s/csv" % occId
   with open(fn, 'w') as f:
      f.write(urllib2.urlopen(url).read())
   
if __name__ == "__main__":
   with open(inNamesFn) as namesF:
      for line in namesF:
         name = line.strip()
         
         occId = getOccIdForName(name)
         if occId is not None:
            outFn = os.path.join(outDir, "%s.csv" % name.replace(' ', '_'))
            try:
               getCsv(occId, outFn)
            except:
               print "Couldn't return %s (%s)" % (name, occId)
   
   