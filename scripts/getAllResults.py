"""
@summary: Gets all results for a particular provider
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
from modules.providers import PROVIDERS
# node, prov #, total #, rank, num providers

# .............................................................................
def getResultsForProvider(node, providerId):
   results = []
   if node['providers'].has_key(providerId):
      numProv = len(node['providers'].keys())
      
      temp = []
      total = 0
      for key in node['providers'].keys():
         temp.append((node['providers'][key], key))
         total += node['providers'][key]
      temp = sorted(temp, reverse=True)
      rank = 0
      for i in xrange(len(temp)):
         if temp[i][1] == providerId:
            rank = i+1
      
      results.append([node['name'], node['providers'][providerId], total, rank, numProv])
      
      if node.has_key('children'):
         for child in node['children']:
            results.extend(getResultsForProvider(child, providerId))
   return results

# .............................................................................
def getSignificantResults(results):
   top1s = []
   top3s = []
   top10per = []
   top25per = []
   highestPer = []
   highestCount = []
   significants = []
   
   for result in results:
      if result[3] == 1:
         top1s.append(result)
      if result[3] <= 3:
         top3s.append(result)
      
      rankPer = 1.0 * result[3] / result[4]
      if rankPer <= 0.10:
         top10per.append([rankPer, result[0], result[1], result[2], result[3], result[4]])
      if rankPer <= 0.25:
         top25per.append([rankPer, result[0], result[1], result[2], result[3], result[4]])
      
      highestPer.append([1.0*result[1]/result[2], result[0], result[1], result[2], result[3], result[4]])
      highestCount.append([result[1], result[0], result[1], result[2], result[3], result[4]])
      
      # (percent contributed - expected) * (number of providers - rank +1)
      sigScore = (1.0*result[1]/result[2] - 1.0*result[3]/result[4]) * (result[4] - result[3] + 1)
      significants.append([sigScore, result[0], result[1], result[2], result[3], result[4]])
   
   top10per.sort()
   top25per.sort()
   highestPer.sort(reverse=True)
   highestCount.sort(reverse=True)
   significants.sort(reverse=True)
   
   print "----------------------------------------------"
   print "-                 Number 1s                  -"
   print "----------------------------------------------"
   for r in top1s:
      print r
   print "----------------------------------------------"
   print "----------------------------------------------"
   print "-                  Top 3ss                   -"
   print "----------------------------------------------"
   for r in top3s:
      print r
   print "----------------------------------------------"
   print "----------------------------------------------"
   print "-                 Top 10 %                   -"
   print "----------------------------------------------"
   for r in top10per:
      print r
   print "----------------------------------------------"
   print "----------------------------------------------"
   print "-                 Top 25 %                   -"
   print "----------------------------------------------"
   for r in top25per:
      print r
   print "----------------------------------------------"
   print "----------------------------------------------"
   print "-                 Highest %                  -"
   print "----------------------------------------------"
   num = 10
   if len(highestPer) < num:
      num = len(highestPer)
   for r in highestPer[:num]:
      print r
   print "----------------------------------------------"
   print "----------------------------------------------"
   print "-               Highest Count                -"
   print "----------------------------------------------"
   num = 10
   if len(highestCount) < num:
      num = len(highestCount)
   for r in highestCount[:num]:
      print r
   print "----------------------------------------------"
   print "----------------------------------------------"
   print "-              Most Significant              -"
   print "----------------------------------------------"
   num = 10
   if len(significants) < num:
      num = len(significants)
   for r in significants[:num]:
      print r
   print "----------------------------------------------"

# .............................................................................
if __name__ == "__main__":
   import json
   providerId = "123"
   
   treeFn = "/home/cjgrady/workspace/occDataMiningPOC/data/tree/mammalsWithStats.json"
   jTree = json.load(open(treeFn))
   
   print "===================================================================="
   print " Report for", PROVIDERS[int(providerId)]
   print "===================================================================="
   
   getSignificantResults(getResultsForProvider(jTree, providerId))
   