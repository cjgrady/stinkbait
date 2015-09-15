"""
@summary: Module to build a taxon tree
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
import json

taxaFns = [
#   "/home/cjgrady/workspace/occDataMiningPOC/data/taxonTree/KuHerpsTax.csv",
#   "/home/cjgrady/workspace/occDataMiningPOC/data/taxonTree/KuMamTax.csv",
   "/home/cjgrady/workspace/occDataMiningPOC/data/taxonTree/KuFishTax.csv",
          ]

outFn = "/home/cjgrady/workspace/occDataMiningPOC/data/taxonTree/fishTaxa.json"
txIdxFn = "/home/cjgrady/workspace/occDataMiningPOC/data/other/fishTaxonIndices.txt"
idx = 0

indices = []
RANKS = {
         "kingdom" : 0,
         "class" : 1,
         "family" : 2,
         "order" : 3,
         "genus" : 4,
         "species" : 5
        }


# .............................................................................
def createNode(name, rank, tName=None):
   global idx
   global indices
   node = {
           "index" : idx,
           "name" : name,
           "rank" : rank,
           "children" : []
          }
   
   indices.append([idx, name, RANKS[rank], tName])
   idx += 1
   
   if tName is not None:
      node['taxon_name'] = tName
   return node

# .............................................................................
if __name__ == "__main__":
   root = createNode("Animalia", "kingdom")
   
   for tFn in taxaFns:
      with open(tFn) as tf:
         reader = csv.reader(tf)
         headers = reader.next()
         for row in reader:
            tClass, tOrder, tFamily, tGenus, tSpecies = row
            
            # Class
            classIdx = None
            for i in xrange(len(root['children'])):
               if root['children'][i]['name'] == tClass:
                  classIdx = i
            if classIdx is None:
               root['children'].append(createNode(tClass, "class"))
               classIdx = len(root['children']) - 1
   
            # Order
            orderIdx = None
            for i in xrange(len(root['children'][classIdx]['children'])):
               if root['children'][classIdx]['children'][i]['name'] == tOrder:
                  orderIdx = i
            if orderIdx is None:
               root['children'][classIdx]['children'].append(createNode(tOrder, "order"))
               orderIdx = len(root['children'][classIdx]['children']) - 1

            # Family
            familyIdx = None
            for i in xrange(len(root['children'][classIdx]['children'][orderIdx]['children'])):
               if root['children'][classIdx]['children'][orderIdx]['children'][i]['name'] == tFamily:
                  familyIdx = i
            if familyIdx is None:
               root['children'][classIdx]['children'][orderIdx]['children'].append(createNode(tFamily, "family"))
               familyIdx = len(root['children'][classIdx]['children'][orderIdx]['children']) - 1

            # Genus
            genusIdx = None
            for i in xrange(len(root['children'][classIdx]['children'][orderIdx]['children'][familyIdx]['children'])):
               if root['children'][classIdx]['children'][orderIdx]['children'][familyIdx]['children'][i]['name'] == tGenus:
                  genusIdx = i
            if genusIdx is None:
               root['children'][classIdx]['children'][orderIdx]['children'][familyIdx]['children'].append(createNode(tGenus, "genus"))
               genusIdx = len(root['children'][classIdx]['children'][orderIdx]['children'][familyIdx]['children']) - 1

            # Species
            root['children'][classIdx]['children'][orderIdx]['children'][familyIdx]['children'][genusIdx]['children'].append(createNode(tSpecies, "species", tName="%s %s" % (tGenus, tSpecies)))
   
   json.dump(root, open(outFn, 'w'), indent=3, separators=(',', ': '))

   with open(txIdxFn, 'w') as txIdxs:
      global indices
      for idx, name, rank, tName in indices:
         if tName is not None:
            name = tName
         txIdxs.write("   %s : {\"name\" : \"%s\", \"rank\" : %s},\n" % (idx, name.replace('"', "'"), rank))
   