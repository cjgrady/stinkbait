"""
@summary: 
@author: CJ Grady
@version: 
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

#result
# provider, taxon id, geometry id, number of points from provider, total number of points, provider rank, number of providers 

def getResults(node, geom):
   results = []
   
   if node.has_key('children'):
      for child in node['children']:
         childrenStats.append(fillProviderStats(child))
      
      for cProviders in childrenStats:
         for key in cProviders:
            if providers.has_key(key):
               providers[key] += cProviders[key]
            else:
               providers[key] = cProviders[key]
