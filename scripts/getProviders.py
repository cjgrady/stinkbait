"""
@summary: Gets all of the providers in all of the CSV files so that they can be mapped
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
provs = ['provname', 'provkey', 'puborgkey']

# Get all collections / resources
import csv
import glob

if __name__ == "__main__":
   providers = set()
   
   pathExp = "/home/cjgrady/workspace/occDataMiningPOC/data/csvs/*.csv"
   
   providers = set()
   
   for fn in glob.iglob(pathExp):
      print "Processing", fn
      with open(fn) as f:
         try:
            reader = csv.reader(f)
            
            headers = reader.next()
            
            provCol = None
            for provKey in provs:
               try:
                  provCol = headers.index(provKey)
               except:
                  pass
                  
            if provCol is not None:
               for row in reader:
                  providers.add(row[provCol])
            else:
               print "   provCol was None"
         except:
            print "Problem with file:", fn
            
   with open("providers.txt", 'w') as f:
      for provider in providers:
         f.write("%s\n" % provider)
         