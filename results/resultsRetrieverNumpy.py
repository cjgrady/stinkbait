"""
@summary: Results retriever written to use numpy
@author: CJ Grady
@version: 2.0
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
import numpy

PROVIDER_FIELD = 0
TAXON_RANK_FIELD = 1
TAXON_FIELD = 2
REGION_FIELD = 3
PROVIDER_PTS_FIELD = 4
TOTAL_PTS_FIELD = 5
RANK_FIELD = 6
NUM_PROV_FIELD = 7

RESULTS_FN = "/home/cjgrady/workspace/occDataMiningPOC/data/results/fishResults2.csv"

# .............................................................................
def _loadAllResults():
   results = numpy.loadtxt(RESULTS_FN, dtype=int, delimiter=',')
   return results

# .............................................................................
def subsetResults(results=None, taxonRank=None, taxonId=None, providerId=None, regionId=None):
   if results is None:
      results = _loadAllResults()
   
   if taxonRank is not None:
      results = results[results[:,TAXON_RANK_FIELD] == int(taxonRank)]
   if taxonId is not None:
      results = results[results[:,TAXON_FIELD] == int(taxonId)]
   if providerId is not None:
      results = results[results[:,PROVIDER_FIELD] == int(providerId)]
   if regionId is not None:
      results = results[results[:,REGION_FIELD] == int(regionId)]

   return results

# .............................................................................
def providerRankedInTopX(results, providerId, x=3, regionId=0, taxonRank=5):
   """
   @summary: Returns an array of results where the provider is ranked in the top 
                X in data provided for the particular taxon in the specified 
                region
   @param results: An array of results to subset
   @param providerId: The id of the provider to pull results for
   @param x: (optional) The number of ranks to pull 
                           (ex. x = 3, return ranks 1, 2, 3)
   @param regionId: (optional) The region to use (0 - global)
   @param taxonRank: (optional) The taxon rank to pull results for, 
                                   None for all, 5 for species
   """
   if results.shape[0] > 0:
      results = results[results[:,PROVIDER_FIELD] == int(providerId)]
   if results.shape[0] > 0:
      results = results[results[:,RANK_FIELD] <= int(x)] # Use less than because rank is zero based
   if results.shape[0] > 0:
      results = results[results[:,REGION_FIELD] == int(regionId)]
   if taxonRank is not None:
      if results.shape[0] > 0:
         results = results[results[:,TAXON_RANK_FIELD] == int(taxonRank)]

   # Sort results
   results = numpy.array(sorted(results, key=lambda x: x[RANK_FIELD]))
   return results

# .............................................................................
def providerOfRareTaxa(results, providerId, rarity=5, regionId=0, taxonRank=5, 
                          maxPoints=None):
   """
   @summary: Returns an array of results where the provider is one of only a 
                few providers for the taxon in the specified region
   @param results: An array of results to subset
   @param providerId: The id of the provider to pull results for
   @param rarity: (optional) The maximum number of providers to classify as 'rare'
   @param regionId: (optional) The region to use (0 - global)
   @param taxonRank: (optional) The taxon rank to pull results for, 
                                   None for all, 5 for species
   @param maxPoints: (optional) The maximum number of total points for a taxon
   """
   try:
      results = results[results[:,PROVIDER_FIELD] == int(providerId)]
      if results.shape[0] > 0:
         results = results[results[:,NUM_PROV_FIELD] <= int(rarity)]
      if results.shape[0] > 0:
         results = results[results[:,REGION_FIELD] == int(regionId)]
      if taxonRank is not None:
         if results.shape[0] > 0:
            results = results[results[:,TAXON_RANK_FIELD] == int(taxonRank)]
      if maxPoints is not None:
         if results.shape[0] > 0:
            results = results[results[:,TOTAL_PTS_FIELD] <= int(maxPoints)]
   
      # Sort results
      results = numpy.array(sorted(results, key=lambda x: x[NUM_PROV_FIELD]))
      return results
   except Exception, e:
      print str(e)
      return []
   
# .............................................................................
def getNumberOfUniqueTaxa(results, providerId=None, regionId=0, taxonRank=5):
   """
   @summary: Gets the number of unique species (only 1 provider) for the 
                specified region and provider
   @param results: An array of results to subset
   @param providerId: (optional) The provider to count unique species for, 
                                  if none, return total for all providers
   @param regionId: (optional) The region to use (0 - global)
   @param taxonRank: (optional) The taxon rank to pull results for, 
                                   None for all, 5 for species
   """
   if results.shape[0] > 0:
      results = results[results[:,NUM_PROV_FIELD] == 1]
   if results.shape[0] > 0:
      results = results[results[:,REGION_FIELD] == int(regionId)]
   if taxonRank is not None:
      if results.shape[0] > 0:
         results = results[results[:,TAXON_RANK_FIELD] == int(taxonRank)]
   if providerId is not None:
      if results.shape[0] > 0:
         results = results[results[:,PROVIDER_FIELD] == int(providerId)]
   
   return results.shape[0]

# .............................................................................
def getNumberOfRareTaxaByPoints(results, providerId=None, maxPoints=10, 
                                regionId=0, taxonRank=5):
   """
   @summary: Returns the number of 'rare' taxa determined by the number of 
                points
   @param results: An array of results to subset
   @param providerId: (optional) The provider to count rare taxa, 
                                  if none, return total for all providers
   @param maxPoints: (optional) The maximum number of points to classify as rare
   @param regionId: (optional) The region to use (0 - global)
   @param taxonRank: (optional) The taxon rank to pull results for, 
                                   None for all, 5 for species
   """
   if results.shape[0] > 0:
      results = results[results[:,TOTAL_PTS_FIELD] <= int(maxPoints)]
   if results.shape[0] > 0:
      results = results[results[:,REGION_FIELD] == int(regionId)]
   if taxonRank is not None:
      if results.shape[0] > 0:
         results = results[results[:,TAXON_RANK_FIELD] == int(taxonRank)]
   if providerId is not None:
      if results.shape[0] > 0:
         results = results[results[:,PROVIDER_FIELD] == int(providerId)]

   return results.shape[0]


# .............................................................................
def getNumberOfRareTaxaByProviders(results, providerId=None, maxProviders=5, 
                                   regionId=0, taxonRank=5):
   """
   @summary: Returns the number of 'rare' taxa determined by the number of 
                providers
   @param results: An array of results to subset
   @param providerId: (optional) The provider to count rare taxa, 
                                  if none, return total for all providers
   @param maxProviders: (optional) The maximum number of providers to classify 
                                      as rare
   @param regionId: (optional) The region to use (0 - global)
   @param taxonRank: (optional) The taxon rank to pull results for, 
                                   None for all, 5 for species
   """
   if results.shape[0] > 0:
      results = results[results[:,NUM_PROV_FIELD] <= int(maxProviders)]
   if results.shape[0] > 0:
      results = results[results[:,REGION_FIELD] == int(regionId)]
   if taxonRank is not None:
      if results.shape[0] > 0:
         results = results[results[:,TAXON_RANK_FIELD] == int(taxonRank)]
   if providerId is not None:
      if results.shape[0] > 0:
         results = results[results[:,PROVIDER_FIELD] == int(providerId)]
   
   return results.shape[0]

# .............................................................................
def getNumberOfTaxaRepresented(results, providerId=None, regionId=0, taxonRank=5):
   """
   @summary: Return the total number of taxa represented
   @param results: An array of results to subset
   @param providerId: (optional) The provider to count rare taxa, 
                                  if none, return total for all providers
   @param regionId: (optional) The region to use (0 - global)
   @param taxonRank: (optional) The taxon rank to pull results for, 
                                   None for all, 5 for species
   """
   if results.shape[0] > 0:
      results = results[results[:,REGION_FIELD] == int(regionId)]
   if taxonRank is not None:
      if results.shape[0] > 0:
         results = results[results[:,TAXON_RANK_FIELD] == int(taxonRank)]
   if providerId is not None:
      if results.shape[0] > 0:
         results = results[results[:,PROVIDER_FIELD] == int(providerId)]
   try:
      uniqueTaxa = numpy.unique(results[:,TAXON_FIELD])
      return uniqueTaxa.shape[0]
   except:
      return 0


# I am ranked in the top 3 for data contributed for species in region
# I am one of the x providers of a species in region (rare for global)
# 
# I have # unique species
# I have # rare species (<= 10 points)
# I ahve # rare species (<= 5 providers)
# I have # of taxa represented
# 


