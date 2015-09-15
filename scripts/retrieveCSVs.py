"""
@summary: Retrieves the CSV files
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
import urllib2

if __name__ == "__main__":
   nameFn = "/home/cjgrady/workspace/occDataMiningPOC/data/other/fishTaxaNamesWithIds.txt"
   
   names = open(nameFn)
   
   for line in names:
      parts = line.strip().split(' : ')
      name = parts[0]
      ids = parts[1].split(' ')
      
      for id in ids:
         url = "http://lifemapper.org/services/sdm/occurrences/%s/csv" % id
         print url
         tmp = "%s%s" % (name.replace(' ', '_'), ids.index(id))
         try:
            with open("/home/cjgrady/workspace/occDataMiningPOC/data/csvs/%s.csv" % tmp, 'w') as f:
               f.write(urllib2.urlopen(url).read())
         except:
            pass
            