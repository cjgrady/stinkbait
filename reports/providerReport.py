"""
@summary: Module containing functions to create a report for a provider
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
from results.resultsRetrieverNumpy import getNumberOfRareTaxaByPoints, \
               getNumberOfRareTaxaByProviders, getNumberOfTaxaRepresented, \
               getNumberOfUniqueTaxa, providerOfRareTaxa, providerRankedInTopX, \
               subsetResults

#from results.resultsRetriever import subsetResults, getHighestCounts, getSignificantResults, getNumber1s, getTop3s, getTop10percents, getTop25percents, getHighestPercents
from dataHelpers.regions import CONTINENTS_LOOKUP, COUNTRIES_LOOKUP, STATES_LOOKUP, OCEANS_LOOKUP
from dataLookups.taxa import TAXA

reportDir = "/home/cjgrady/workspace/occDataMiningPOC/data/reports/fish/provider/"

def generateProviderReport(results, providerId):
   results = subsetResults(results=results, providerId=providerId)
   fn = os.path.join(reportDir, "%s.html" % str(providerId))
   
   with open(fn, 'w') as outF:
      outF.write('<html>\n')
      outF.write('   <head>\n')
      outF.write('      <title>Report for %s</title>\n' % (PROVIDERS[providerId]))
      outF.write('   </head>\n')
      outF.write('   <body>\n')
      outF.write('      <h1>Provider report for: %s</h1>\n' % (PROVIDERS[providerId]))
      outF.write('      <br /><br />\n')
      
      outF.write('      <table>\n')
      # I have # unique species
      outF.write('         <tr>\n')
      outF.write('            <th>Number of unique species:</th>\n')
      outF.write('            <td>%s</td>\n' % getNumberOfUniqueTaxa(results, providerId=providerId))
      outF.write('         </tr>\n')
      # I have # rare species ( <= 10 points)
      outF.write('         <tr>\n')
      outF.write('            <th>Number of rare species (&lt;= 10 points)</th>\n')
      outF.write('            <td>%s</td>\n' % getNumberOfRareTaxaByPoints(results, providerId=providerId))
      outF.write('         </tr>\n')
      # I have # rare species ( <= 5 providers)
      outF.write('         <tr>\n')
      outF.write('            <th>Number of rare species (&lt;= 5 providers)</th>\n')
      outF.write('            <td>%s</td>\n' % getNumberOfRareTaxaByProviders(results, providerId=providerId))
      outF.write('         </tr>\n')
      # I have # of taxa represented
      outF.write('         <tr>\n')
      outF.write('            <th>Number of taxa represented</th>\n')
      outF.write('            <td>%s</td>\n' % getNumberOfTaxaRepresented(results, providerId=providerId))
      outF.write('         </tr>\n')
      outF.write('      </table>\n')
         
      
      # I am ranked in the top 3 for data contributed for:
      globalTopContrib = providerRankedInTopX(results, providerId)
      outF.write('      <h2>I am ranked in the top 3 for data contributed to these species globally</h2>\n')
      outF.write('      <ul>\n')
      for r in globalTopContrib:
         outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[6]))
      outF.write('      </ul>\n')
      outF.write('      <br /><br />\n')
      

      # I am one of x providers of species
      globalProvRareSpecies = providerOfRareTaxa(results, providerId, maxPoints=10)
      outF.write('      <h2>I am one of X providers of these species globally</h2>\n')
      outF.write('      <ul>\n')
      for r in globalProvRareSpecies:
         outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[7]))
      outF.write('      </ul>\n')
      outF.write('      <br /><br />\n')


      
      # Regionally
      # I am ranked in the top 3 for data contributed for:

      # I am one of x providers of species

      # For each continent
      outF.write('      <h2>Continents</h2>\n')
      for k in CONTINENTS_LOOKUP:
         regionId = CONTINENTS_LOOKUP[k]
         regionMostContrib = providerRankedInTopX(results, providerId, regionId=regionId)
         regionRareProv = providerOfRareTaxa(results, providerId, regionId=regionId)
         
         if len(regionMostContrib) > 0 or len(regionRareProv) > 0:
            outF.write('      <h3>%s</h3>\n' % k)
            outF.write('      <table>\n')
            outF.write('         <tr>\n')
            outF.write('            <td>\n')
            
            # I am ranked in the top 3 for data contributed for:
            if len(regionMostContrib) > 0:
               outF.write('               <b>I am one of the top 3 contributers in the region for:</b>\n')
               outF.write('               <ul>\n')
               for r in regionMostContrib:
                  outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[6]))
               outF.write('               </ul>\n')
            else:
               outF.write('               &nbsp;\n')

            outF.write('            </td>\n')
            outF.write('            <td>\n')

            # I am one of x providers of species
            if len(regionRareProv) > 0:
               outF.write('               <b>I am one of X providers of these species in this region:</b>\n')
               outF.write('               <ul>\n')
               for r in regionRareProv:
                  outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[7]))
               outF.write('               </ul>\n')
            else:
               outF.write('               &nbsp;\n')

            outF.write('            </td>\n')
            outF.write('         </tr>\n')
            outF.write('      </table>\n')
      outF.write('      <br /><br />\n')

      # For each country
      outF.write('      <h2>Countries Top 10</h2>\n')
      for k in COUNTRIES_LOOKUP:
         regionId = COUNTRIES_LOOKUP[k]
         regionMostContrib = providerRankedInTopX(results, providerId, regionId=regionId)
         regionRareProv = providerOfRareTaxa(results, providerId, regionId=regionId)
         
         if len(regionMostContrib) > 0 or len(regionRareProv) > 0:
            outF.write('      <h3>%s</h3>\n' % k)
            outF.write('      <table>\n')
            outF.write('         <tr>\n')
            outF.write('            <td>\n')
            
            # I am ranked in the top 3 for data contributed for:
            if len(regionMostContrib) > 0:
               outF.write('               <b>I am one of the top 3 contributers in the region for:</b>\n')
               outF.write('               <ul>\n')
               for r in regionMostContrib:
                  outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[6]))
               outF.write('               </ul>\n')
            else:
               outF.write('               &nbsp;\n')

            outF.write('            </td>\n')
            outF.write('            <td>\n')

            # I am one of x providers of species
            if len(regionRareProv) > 0:
               outF.write('               <b>I am one of X providers of these species in this region:</b>\n')
               outF.write('               <ul>\n')
               for r in regionRareProv:
                  outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[7]))
               outF.write('               </ul>\n')
            else:
               outF.write('               &nbsp;\n')

            outF.write('            </td>\n')
            outF.write('         </tr>\n')
            outF.write('      </table>\n')
      outF.write('      <br /><br />\n')
      
      # For each state
      outF.write('      <h2>States Top 10</h2>\n')
      for k in STATES_LOOKUP:
         regionId = STATES_LOOKUP[k]
         regionMostContrib = providerRankedInTopX(results, providerId, regionId=regionId)
         regionRareProv = providerOfRareTaxa(results, providerId, regionId=regionId)
         
         if len(regionMostContrib) > 0 or len(regionRareProv) > 0:
            outF.write('      <h3>%s</h3>\n' % k)
            outF.write('      <table>\n')
            outF.write('         <tr>\n')
            outF.write('            <td>\n')
            
            # I am ranked in the top 3 for data contributed for:
            if len(regionMostContrib) > 0:
               outF.write('               <b>I am one of the top 3 contributers in the region for:</b>\n')
               outF.write('               <ul>\n')
               for r in regionMostContrib:
                  outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[6]))
               outF.write('               </ul>\n')
            else:
               outF.write('               &nbsp;\n')

            outF.write('            </td>\n')
            outF.write('            <td>\n')

            # I am one of x providers of species
            if len(regionRareProv) > 0:
               outF.write('               <b>I am one of X providers of these species in this region:</b>\n')
               outF.write('               <ul>\n')
               for r in regionRareProv:
                  outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[7]))
               outF.write('               </ul>\n')
            else:
               outF.write('               &nbsp;\n')

            outF.write('            </td>\n')
            outF.write('         </tr>\n')
            outF.write('      </table>\n')
      outF.write('      <br /><br />\n')
     
      # For each ocean
      outF.write('      <h2>Oceans Top 10</h2>\n')
      for k in OCEANS_LOOKUP:
         regionId = OCEANS_LOOKUP[k]
         regionMostContrib = providerRankedInTopX(results, providerId, regionId=regionId)
         regionRareProv = providerOfRareTaxa(results, providerId, regionId=regionId)
         
         if len(regionMostContrib) > 0 or len(regionRareProv) > 0:
            outF.write('      <h3>%s</h3>\n' % k)
            outF.write('      <table>\n')
            outF.write('         <tr>\n')
            outF.write('            <td>\n')
            
            # I am ranked in the top 3 for data contributed for:
            if len(regionMostContrib) > 0:
               outF.write('               <b>I am one of the top 3 contributers in the region for:</b>\n')
               outF.write('               <ul>\n')
               for r in regionMostContrib:
                  outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[6]))
               outF.write('               </ul>\n')
            else:
               outF.write('               &nbsp;\n')

            outF.write('            </td>\n')
            outF.write('            <td>\n')

            # I am one of x providers of species
            if len(regionRareProv) > 0:
               outF.write('               <b>I am one of X providers of these species in this region:</b>\n')
               outF.write('               <ul>\n')
               for r in regionRareProv:
                  outF.write('         <li>%s - %s</li>\n' % (TAXA[r[2]]['name'], r[7]))
               outF.write('               </ul>\n')
            else:
               outF.write('               &nbsp;\n')

            outF.write('            </td>\n')
            outF.write('         </tr>\n')
            outF.write('      </table>\n')
      outF.write('      <br /><br />\n')
      
      outF.write('   </body>\n')
      outF.write('</html>')
   
# .............................................................................
if __name__ == "__main__":
   results = subsetResults()
   for k in PROVIDERS:
      print PROVIDERS[k]
      generateProviderReport(results, k)
