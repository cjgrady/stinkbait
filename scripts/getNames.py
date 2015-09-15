"""
@summary: Gets all of the names out of the tree
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
import json

fn = "/home/cjgrady/workspace/occDataMiningPOC/data/tree/mammals.json"

def getNames(el):
   names = []
   if el['name'] != u'':
      names.append(el['name'])
   try:
      for child in el['children']:
         names.extend(getNames(child))
   except:
      pass
   return names

if __name__ == "__main__":
   gDict = json.load(open(fn))
   
   names = getNames(gDict)
   
   outFn = "/home/cjgrady/workspace/occDataMiningPOC/data/names.txt"
   with open(outFn, 'w') as f:
      for name in names:
         f.write('%s\n' % name.replace('_', ' '))
   