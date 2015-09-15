"""
@summary: Script to build a tree that includes count data for each level
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
import os

# For each node
# Get sums from children
# Total sum
# Add providers to node

treeFn = "/home/cjgrady/workspace/occDataMiningPOC/data/tree/mammals.json"
outTreeFn = "/home/cjgrady/workspace/occDataMiningPOC/data/tree/mammalsWithStats.json"

csvsPath = "/home/cjgrady/workspace/occDataMiningPOC/data/modCSVs"

unnamedNode = 1

# .............................................................................
def fillProviderStats(node):
   providers = {}
   name = node.get('name')
   if len(name) == 0:
      global unnamedNode
      name = "Node%s" % unnamedNode
      unnamedNode += 1
      node['name'] = name
   
   
   # Look for csv file and populate providers
   fn = os.path.join(csvsPath, "%s.csv" % name)
   if os.path.exists(fn):
      with open(fn) as f:
         reader = csv.reader(f)
         headers = reader.next()
         
         for row in reader:
            prov = int(row[2])
            if providers.has_key(prov):
               providers[prov] += 1
            else:
               providers[prov] = 1
         
   # Add children
   childrenStats = []
   if node.has_key('children'):
      for child in node['children']:
         childrenStats.append(fillProviderStats(child))
      
      for cProviders in childrenStats:
         for key in cProviders:
            if providers.has_key(key):
               providers[key] += cProviders[key]
            else:
               providers[key] = cProviders[key]
   
   node['providers'] = providers
   return providers

# .............................................................................
if __name__ == "__main__":
   jTree = json.load(open(treeFn))
   totalsDict = fillProviderStats(jTree)
   json.dump(jTree, open(outTreeFn, 'w'))
   print totalsDict
   