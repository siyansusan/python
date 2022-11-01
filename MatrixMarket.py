#!/usr/bin/env python
#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Author: William H. Majoros (bmajoros@alumni.duke.edu)
# Author(10/31/2022): Susan Liu
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import sys
import ProgramName
import gzip
from Rex import Rex
rex=Rex()

#=========================================================================
# Attributes:
#    filename: string
#    header : array of int
#    col_index: int
#    groups_generator: generator of array
# Instance Methods:
#    MatrixMarket(filename)
#    get_groups(self)
#    nextGroup(self,colIndex)
#    getHeader()
# Class Methods:
#    allGroups=loadFile(filename,colIndex)
#=========================================================================
class MatrixMarket:
    def __init__(self, filename):
        self.filename = filename

        self.header = None

        self.col_index = None
        self.groups_generator = None

    def get_groups(self):

        #find file opening function
        if self.filename.endswith(".gz"):
            open_func = gzip.open
        else:
            open_func = open

        with open_func(self.filename, "rt") as fh:

            #skip first line of header
            fh.readline()

            #read totals
            line = fh.readline()
            self.header = [int(x) for x in line.rstrip().split()]

            #initialize current ID and group
            cur_ID = None
            group = []

            #continue reading groups
            for line in fh:

                fields = line.rstrip().split()
                
                if cur_ID is None:
                    cur_ID = fields[self.col_index]

                if cur_ID != fields[self.col_index]:
                    yield group

                    cur_ID = fields[self.col_index]
                    group = [fields]

                else:
                    group.append(fields)

            #yield the last group
            yield group

    def nextGroup(self, colIndex):

        #initialize group generator
        if self.groups_generator is None:
            self.col_index = colIndex
            self.groups_generator = self.get_groups()
        
        try:
            return next(self.groups_generator)
        except StopIteration:
            return None

    def getHeader(self):
        return self.header

    @classmethod
    def loadFile(self,filename,colIndex):
        reader=MatrixMarket(filename)
        groups=[]
        while(True):
            group=reader.nextGroup(colIndex)
            if(group is None): break
            groups.append(group)
        return groups
