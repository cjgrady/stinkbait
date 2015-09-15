"""
@summary: Module containing functions to generate taxon reports
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

from modules.providers import PROVIDERS 
from results.resultsRetriever import subsetResults, getHighestCounts
from dataHelpers.regions import CONTINENTS_LOOKUP, COUNTRIES_LOOKUP, STATES_LOOKUP, OCEANS_LOOKUP

reportDir = "/home/cjgrady/workspace/occDataMiningPOC/data/reports/fish/taxon/"

def generateTaxonReport(tNode, results, subDirectory):
   workingResults = subsetResults(taxonId=int(tNode['index']))
   fn = "report.html"
   
   baseDir = os.path.join(reportDir, subDirectory)
   print baseDir
   
   # Make directory if it does not exist
   if not os.path.exists(baseDir):
      os.makedirs(baseDir)
   
   outFn = os.path.join(baseDir, fn)
   with open(outFn, 'w') as outF:
      outF.write('<html>\n')
      outF.write('   <head>\n')
      outF.write('      <title>Report for %s - %s</title>\n' % (tNode['rank'], tNode['name']))
      outF.write('   </head>\n')
      outF.write('   <body>\n')
      outF.write('      <h1>%s - %s</h1>\n' % (tNode['rank'], tNode['name']))
      if tNode.has_key('taxon_name'):
         outF.write('      <h3>Taxon Name: %s</h3>\n' % tNode['taxon_name'])
      
      outF.write('      <br /><br />\n')
      
      # Write out children
      if tNode.has_key('children'):
         outF.write('      <h2>Children</h2>\n')
         outF.write('      <ul>\n')
         for child in tNode['children']:
            sDir = '%s/%s' % (subDirectory, child['name'])
            try:
               outF.write('         <li><a href="%s/report.html">%s</a></li>\n' % (sDir, child['name']))
            except:
               pass
            generateTaxonReport(child, results, sDir)
         outF.write('      </ul>\n')
         outF.write('      <br /><br />\n')
      
      # Global top 10
      top10 = getHighestCounts(workingResults)
      outF.write('      <h2>Global Top 10</h2>\n')
      outF.write('      <ol>\n')
      for r in top10:
         try:
            outF.write('         <li>%s : %s</li>\n' % (PROVIDERS[r[0]], r[3]))
         except:
            pass
      outF.write('      </ol>\n')
      
      outF.write('      <br /><br />\n')

      # For each continent
      outF.write('      <h2>Continents Top 10</h2>\n')
      for k in CONTINENTS_LOOKUP:
         regionId = CONTINENTS_LOOKUP[k]
         continentTop10 = getHighestCounts(subsetResults(results=workingResults, regionId=regionId))
         if len(continentTop10) > 0:
            outF.write('      <h3>%s</h3>\n' % k)
            outF.write('      <ol>\n')
            for r in continentTop10:
               try:
                  outF.write('         <li>%s : %s</li>\n' % (PROVIDERS[r[0]], r[3]))
               except:
                  pass
            outF.write('      </ol>\n')
            outF.write('      <br /><br />')
      
      outF.write('      <br /><br />\n')

      # For each country
      outF.write('      <h2>Countries Top 10</h2>\n')
      for k in COUNTRIES_LOOKUP:
         regionId = COUNTRIES_LOOKUP[k]
         countryTop10 = getHighestCounts(subsetResults(results=workingResults, regionId=regionId))
         if len(countryTop10) > 0:
            outF.write('      <h3>%s</h3>\n' % k)
            outF.write('      <ol>\n')
            for r in countryTop10:
               try:
                  outF.write('         <li>%s : %s</li>\n' % (PROVIDERS[r[0]], r[3]))
               except:
                  pass
            outF.write('      </ol>\n')
            outF.write('      <br /><br />\n')
      
      outF.write('      <br /><br />\n')
      
      # For each state
      outF.write('      <h2>States Top 10</h2>\n')
      for k in STATES_LOOKUP:
         regionId = STATES_LOOKUP[k]
         statesTop10 = getHighestCounts(subsetResults(results=workingResults, regionId=regionId))
         if len(statesTop10) > 0:
            outF.write('      <h3>%s</h3>\n' % k)
            outF.write('      <ol>\n')
            for r in statesTop10:
               try:
                  outF.write('         <li>%s : %s</li>\n' % (PROVIDERS[r[0]], r[3]))
               except:
                  pass
            outF.write('      </ol>\n')
            outF.write('      <br /><br />\n')
      
      # For each ocean
      outF.write('      <h2>Oceans Top 10</h2>\n')
      for k in OCEANS_LOOKUP:
         regionId = OCEANS_LOOKUP[k]
         oceansTop10 = getHighestCounts(subsetResults(results=workingResults, regionId=regionId))
         if len(oceansTop10) > 0:
            outF.write('      <h3>%s</h3>\n' % k)
            outF.write('      <ol>\n')
            for r in oceansTop10:
               try:
                  outF.write('         <li>%s : %s</li>\n' % (PROVIDERS[r[0]], r[3]))
               except:
                  pass
            outF.write('      </ol>\n')
            outF.write('      <br /><br />\n')
      
      outF.write('   </body>\n')
      outF.write('</html>')
   
# .............................................................................
if __name__ == "__main__":
   import json
   taxTreeFn = "/home/cjgrady/workspace/occDataMiningPOC/data/taxonTree/fishTaxa.json"
   
   # May need to make directories first
   with open(taxTreeFn) as taxF:
      taxonTree = json.load(taxF)
      results = subsetResults()
      generateTaxonReport(taxonTree, results, reportDir)