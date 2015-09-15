"""
@summary: Gets the occurrence set ids for a list of names, only writes the 
             names to the output file if there are occurrence sets in Lifemapper
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

from LmServer.common.log import ConsoleLogger
from LmServer.db.peruser import Peruser

namesFn = ""
outFn = ""

if __name__ == "__main__":
   
   peruser = Peruser(ConsoleLogger())
   peruser.openConnections()
   
   names = open(namesFn)
   output = open(outFn, 'w')
   
   for name in names:
      occAtoms = peruser.listOccurrenceSets(0, 10, displayName=name.strip())
      if len(occAtoms) > 0:
         output.write('%s : %s\n' % (name.strip(), ' '.join([str(occ.id) for occ in occAtoms])))
   
   output.close()
   
   peruser.closeConnections()
   