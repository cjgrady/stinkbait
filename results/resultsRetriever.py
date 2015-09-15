"""
@summary: Module containing functions to retrieve results
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

PROVIDER_FIELD = 0
TAXON_RANK_FIELD = 1
TAXON_FIELD = 2
REGION_FIELD = 3
PROVIDER_PTS_FIELD = 4
TOTAL_PTS_FIELD = 5
RANK_FIELD = 6
NUM_PROV_FIELD = 7

RESULTS_FN = "/home/cjgrady/workspace/occDataMiningPOC/data/results/fishResults.csv"

# .............................................................................
def _loadAllResults():
   results = []
   with open(RESULTS_FN) as resF:
      reader = csv.reader(resF)

      for line in reader:
         provider = int(line[PROVIDER_FIELD])
         taxonRank = int(line[TAXON_RANK_FIELD])
         taxon = int(line[TAXON_FIELD])
         region = int(line[REGION_FIELD])
         provPts = int(line[PROVIDER_PTS_FIELD])
         totPts = int(line[TOTAL_PTS_FIELD])
         rank = int(line[RANK_FIELD])
         numProv = int(line[NUM_PROV_FIELD])
         
         results.append([provider, taxonRank, taxon, region, provPts, totPts, rank, numProv])
   return results

# .............................................................................
def subsetResults(results=None, taxonRank=None, taxonId=None, providerId=None, regionId=None):
   if results is None:
      results = _loadAllResults()
   
   retResults = []
   
   for res in results:
      if (taxonRank is None or res[TAXON_RANK_FIELD] == taxonRank) and \
            (taxonId is None or res[TAXON_FIELD] == taxonId) and \
            (providerId is None or res[PROVIDER_FIELD] == providerId) and \
            (regionId is None or res[REGION_FIELD] == regionId):
         retResults.append(res)
   
   return retResults

# .............................................................................
def getNumber1s(results):
   retResults = []
   for res in results:
      if res[RANK_FIELD] == 1:
         retResults.append(res)
   return retResults

# .............................................................................
def getTop3s(results):
   retResults = []
   for res in results:
      if res[RANK_FIELD] <= 3:
         retResults.append(res)
   return retResults

# .............................................................................
def getTop10percents(results):
   retResults = []
   for res in results:
      p = 1.0 * res[RANK_FIELD] / res[NUM_PROV_FIELD]
      if p <= 0.10:
         retResults.append(res)
   return retResults

# .............................................................................
def getTop25percents(results):
   retResults = []
   for res in results:
      p = 1.0 * res[RANK_FIELD] / res[NUM_PROV_FIELD]
      if p <= 0.25:
         retResults.append(res)
   return retResults

# .............................................................................
def getHighestCounts(results, x=10):
   def cmpFunc(x, y):
      if x[PROVIDER_PTS_FIELD] < y[PROVIDER_PTS_FIELD]:
         return -1
      elif x[PROVIDER_PTS_FIELD] == y[PROVIDER_PTS_FIELD]:
         return 0
      else:
         return 1
   
   results.sort(cmp=cmpFunc, reverse=True)
   return results[:min(x, len(results))]

# .............................................................................
def getHighestPercents(results, x=10):
   def cmpFunc(x, y):
      xp = 1.0 * x[PROVIDER_PTS_FIELD] / x[TOTAL_PTS_FIELD]
      yp = 1.0 * y[PROVIDER_PTS_FIELD] / y[TOTAL_PTS_FIELD]
      if xp < yp:
         return -1
      elif xp == yp:
         return 0
      else:
         return 1
   
   results.sort(cmp=cmpFunc, reverse=True)
   return results[:min(x, len(results))]

# .............................................................................
def getSignificantResults(results, x=10):
   def sigScore(y):
      # (percent contributed - expected) * (number of providers - rank +1)
      perContrib = 100.0 * y[PROVIDER_PTS_FIELD] / y[TOTAL_PTS_FIELD]
      expectedContrib = 100.0 / y[NUM_PROV_FIELD]
      
      score = (perContrib - expectedContrib) * (y[NUM_PROV_FIELD] - y[RANK_FIELD] + 1)
      return score

   res = []
   for r in results:
      res.append([sigScore(r), r])
      
   res.sort(reverse=True)
   return res[:min(x, len(res))]
