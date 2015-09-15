"""
@summary: Script to rewrite all csvs into smaller files with just lat / long / provider
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
import csv
import glob

from modules.providers import PROVIDERS, PROVIDER_MAPPINGS
from modules.unicodeCsv import UnicodeReader, UnicodeWriter

iDir = "/home/cjgrady/workspace/occDataMiningPOC/data/csvs/"
oDir = "/home/cjgrady/workspace/occDataMiningPOC/data/modFishCsvs/"
namesFn = "/home/cjgrady/workspace/occDataMiningPOC/data/other/fishTaxaNames.txt"

lats = ['lat', 'dec_lat']
lons = ['lon', 'dec_long']
provs = ['provname', 'provkey', 'puborgkey']


if __name__ == "__main__":
   
   print "start"
   with open(namesFn) as namesF:
      for line in namesF:
         name = line.strip().replace(' ', '_')
         print name
         
         pathExp = "%s%s*.csv" % (iDir, name)
         fns = glob.glob(pathExp)
         if len(fns) > 0:
            outFn = "%s%s.csv" % (oDir, name)
            
            with open(outFn, 'w') as outF:
               writer = csv.writer(outF)
               writer.writerow(['lat', 'lon', 'provider'])
            
               for fn in fns:
                  try:
                     with open(fn) as inF:
                        reader = csv.reader(inF)
                        headers = reader.next()
                        
                        # Get needed columns
                        latCol = None
                        lonCol = None
                        provCol = None
                        
                        for latKey in lats:
                           try:
                              latCol = headers.index(latKey)
                           except:
                              pass
                        
                        for lonKey in lons:
                           try:
                              lonCol = headers.index(lonKey)
                           except:
                              pass
                        
                        for provKey in provs:
                           try:
                              provCol = headers.index(provKey)
                           except:
                              pass
                        
                        if provCol is not None and latCol is not None and lonCol is not None:
                           
                           for row in reader:
                              lat = row[latCol]
                              lon = row[lonCol]
                              prov = row[provCol]
                              try:
                                 prov = int(prov)
                              except:
                                 prov = PROVIDER_MAPPINGS[prov]
                              
                              writer.writerow([lat, lon, str(prov)])
                  except Exception, e:
                     print e
            
            #
            
