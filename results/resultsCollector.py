"""
@summary: Module containing a tool to collect results
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

from dataHelpers.regions import CONTINENTS_LOOKUP, COUNTRIES_LOOKUP, STATES_LOOKUP, OCEANS_LOOKUP
from modules.providers import AGGREGATORS


BASE_DATA_DIR = "/home/cjgrady/workspace/occDataMiningPOC/data/"

# Result format: provider, taxon, region, provider points, total points, rank, number of providers

RANKS = {
         "kingdom" : 0,
         "class" : 1,
         "family" : 2,
         "order" : 3,
         "genus" : 4,
         "species" : 5
        }

# .............................................................................
def processCsvFile(fn, taxonRank, taxonId, regionId, continentId=None, countryId=None, stateId=None, oceanId=None):
   results = []
   providers = {}

   try:
      if os.path.exists(fn):
         with open(fn) as f:
            reader = csv.reader(f)
            _ = reader.next()
            
            for row in reader:
               try:
                  provider = int(row[0])
                  continent = int(row[1])
                  country = int(row[2])
                  state = int(row[3])
                  ocean = int(row[4])
               
                  if (continentId is None or continent == continentId) and \
                     (countryId is None or country == countryId) and \
                     (stateId is None or state == stateId) and \
                     (oceanId is None or ocean == oceanId):
   
                     if provider not in AGGREGATORS:
                        if providers.has_key(provider):
                           providers[provider] += 1
                        else:
                           providers[provider] = 1
               except Exception, e:
                  pass
                  #print str(e)
                  #print fn, row
   except Exception, e:
      #pass
      print str(e)
   # --------------------------
   
   numProviders = len(providers.keys())
   totalPoints = sum([providers[k] for k in providers.keys()])
   
   tmp = [(providers[k], k) for k in providers.keys()]
   tmp.sort(reverse=True)
   
   for i in xrange(len(tmp)):
      v, p = tmp[i]
      results.append([p, taxonRank, taxonId, regionId, v, totalPoints, i+1, numProviders])
   
   # --------------------------
   
   return results, providers

# .............................................................................
def getResultsForNode(node, regionId, continentId=None, countryId=None, stateId=None, oceanId=None):
   results = []
   providers = {}
   taxonId = node['index']
   taxonRank = RANKS[node['rank']]
   
   # if taxon name - process file
   if node.has_key('taxon_name'):
      tName = node['taxon_name']
      fn = os.path.join(BASE_DATA_DIR, "fishCsvs", "%s.csv" % tName.replace(' ', '_'))
      res, prov = processCsvFile(fn, taxonRank, taxonId, regionId, continentId=continentId, countryId=countryId, stateId=stateId, oceanId=oceanId)
      results.extend(res)
      
      for key in prov.keys():
         if key not in AGGREGATORS:
            if providers.has_key(key):
               providers[key] += prov[key]
            else:
               providers[key] = prov[key]
   else:
      if node.has_key('children'):
         for child in node['children']:
            res, prov = getResultsForNode(child, regionId, continentId=continentId, countryId=countryId, stateId=stateId, oceanId=None)
            
            results.extend(res)
            
            for k in prov.keys():
               if k not in AGGREGATORS:
                  if providers.has_key(k):
                     providers[k] += prov[k]
                  else:
                     providers[k] = prov[k]
            
      # Build results
      numProviders = len(providers.keys())
      totalPoints = sum([providers[k] for k in providers.keys()])
      
      tmp = [(providers[k], k) for k in providers.keys()]
      tmp.sort(reverse=True)
      
      for i in xrange(len(tmp)):
         p, v = tmp[i]
         results.append([p, taxonRank, taxonId, regionId, v, totalPoints, i, numProviders])
   
   return results, providers


# .............................................................................
if __name__ == "__main__":
   import csv
   import json
   
   treeFn = os.path.join(BASE_DATA_DIR, 'taxonTree', 'fishTaxa.json')
   resultsFn = os.path.join(BASE_DATA_DIR, 'results', 'fishResults2.csv')
   
   with open(treeFn) as treeF:
      tNode = json.load(treeF)
   
      # Global
      results, _ = getResultsForNode(tNode, 0)
      
      with open(resultsFn, 'w') as resF:
         writer = csv.writer(resF)
         print "Writing global results"
         for res in results:
            writer.writerow(res)
   
         # For each continent
         for k in CONTINENTS_LOOKUP:
            print " Continent -", k
            regionId = CONTINENTS_LOOKUP[k]
            results, _ = getResultsForNode(tNode, regionId, continentId=regionId)
            for res in results:
               writer.writerow(res)
         
         # For each country
         for k in COUNTRIES_LOOKUP:
            print " Country -", k
            regionId = COUNTRIES_LOOKUP[k]
            results, _ = getResultsForNode(tNode, regionId, countryId=regionId)
            for res in results:
               writer.writerow(res)
      
         # For each state
         for k in STATES_LOOKUP:
            print " State -", k
            regionId = STATES_LOOKUP[k]
            results, _ = getResultsForNode(tNode, regionId, stateId=regionId)
            for res in results:
               writer.writerow(res)
         
         # For each state
         for k in OCEANS_LOOKUP:
            print " Ocean -", k
            regionId = OCEANS_LOOKUP[k]
            results, _ = getResultsForNode(tNode, regionId, oceanId=regionId)
            for res in results:
               writer.writerow(res)
      