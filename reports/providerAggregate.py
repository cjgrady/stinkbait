"""
@summary: Creates a report with comparative statistics across providers
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
from results.resultsRetrieverNumpy import getNumberOfRareTaxaByPoints, \
               getNumberOfRareTaxaByProviders, getNumberOfTaxaRepresented, \
               getNumberOfUniqueTaxa, providerOfRareTaxa, providerRankedInTopX, \
               subsetResults

outFn = "/home/cjgrady/workspace/occDataMiningPOC/data/reports/fish/providers.html"

if __name__ == "__main__":
   numUnique = []
   numRareSpecies = []
   numRareProv = []
   numTaxa = []
   
   results = subsetResults()
   for k in PROVIDERS:
      print PROVIDERS[k]
      nUnique = getNumberOfUniqueTaxa(results, providerId=k)
      nRareSp = getNumberOfRareTaxaByPoints(results, providerId=k)
      nRareP = getNumberOfRareTaxaByProviders(results, providerId=k)
      numTax = getNumberOfTaxaRepresented(results, providerId=k)
      
      numUnique.append((nUnique, k))
      numRareSpecies.append((nRareSp, k))
      numRareProv.append((nRareP, k))
      numTaxa.append((numTax, k))

   numUnique.sort(reverse=True)
   numRareSpecies.sort(reverse=True)
   numRareProv.sort(reverse=True)
   numTaxa.sort(reverse=True)
   
   
   with open(outFn, 'w') as outF:
      outF.write('<html>\n')
      outF.write('   <head>\n')
      outF.write('      <title>Providers report</title>\n')
      outF.write('   </head>\n')
      outF.write('   <body>\n')
      # Unique
      outF.write('      <h1>Most unique taxa</h1>\n')
      outF.write('      <ol>\n')
      for n, k in numUnique:
         outF.write('         <li>%s - %s</li>\n' % (PROVIDERS[k], n))
      outF.write('      </ol>\n')
      outF.write('      <br /><br />')

      # Rare by species
      outF.write('      <h1>Most rare species (<= 10 points)</h1>\n')
      outF.write('      <ol>\n')
      for n, k in numRareSpecies:
         outF.write('         <li>%s - %s</li>\n' % (PROVIDERS[k], n))
      outF.write('      </ol>\n')
      outF.write('      <br /><br />')
      
      # Rare by provider
      outF.write('      <h1>Most rare species (<= 5 providers)</h1>\n')
      outF.write('      <ol>\n')
      for n, k in numRareProv:
         outF.write('         <li>%s - %s</li>\n' % (PROVIDERS[k], n))
      outF.write('      </ol>\n')
      outF.write('      <br /><br />')
      
      # Number of taxa
      outF.write('      <h1>Number of species</h1>\n')
      outF.write('      <ol>\n')
      for n, k in numTaxa:
         outF.write('         <li>%s - %s</li>\n' % (PROVIDERS[k], n))
      outF.write('      </ol>\n')
      outF.write('      <br /><br />')
      
      outF.write('   </body>\n')
      outF.write('</html>\n')
      
