"""
@summary: This module contains a script to fill in the taxonomic names with something more informative
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
import os

DATA_DIR = "/home/cjgrady/workspace/occDataMiningPOC/data"

def processNode(node):
   ret = []
   if node.has_key('taxon_name'):
      ret.append([node['index'], node['taxon_name']])
   else:
      ret.append([node['index'], "%s - %s" % (node['rank'], node['name'])])
   
   if node.has_key('children'):
      for child in node['children']:
         ret.extend(processNode(child))
   
   return ret

if __name__ == "__main__":
   import json
   taxaTreeFn = os.path.join(DATA_DIR, "taxonTree", "taxa.json")
   outFn = os.path.join(DATA_DIR, "other", "taxaDict.txt")
   with open(taxaTreeFn) as taxF:
      node = json.load(taxF)

      namesList = processNode(node)
      with open(outFn, 'w') as outF:
         for item in namesList:
            outF.write('   %s : "%s",\n' % (item[0], item[1]))


# Load tree
# For each node in tree
#   Add id and better name into a list
#   Recurse into sub trees

# Take list and output a dictionary
