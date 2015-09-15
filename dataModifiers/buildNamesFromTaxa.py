"""
@summary: Module containing functions to build a names list from taxon csv files
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

taxaFns = [
   #"/home/cjgrady/workspace/occDataMiningPOC/data/taxonTree/KuHerpsTax.csv",
   #"/home/cjgrady/workspace/occDataMiningPOC/data/taxonTree/KuMamTax.csv",
   "/home/cjgrady/workspace/occDataMiningPOC/data/taxonTree/KuFishTax.csv"
          ]

namesFn = "/home/cjgrady/workspace/occDataMiningPOC/data/other/fishTaxaNames.txt"

if __name__ == "__main__":
   with open(namesFn, 'w') as namesOut:
      for taxaFn in taxaFns:
         with open(taxaFn) as taxaF:
            reader = csv.reader(taxaF)
            headers = reader.next()
            for row in reader:
               namesOut.write("%s %s\n" % (row[3].strip(), row[4].strip()))
               