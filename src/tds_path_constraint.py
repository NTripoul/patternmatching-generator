#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 02:19:34 2018

@author: qiu
"""
from graphUtils import *

class TdsPathConstraint():
    def __init__(self, subgraph, fromMerge):
        
        self.size=subgraph.number_of_nodes()
        self.subgraph=subgraph
        self.fromMerge=fromMerge
                
    def __str__(self):
        return 'length : \t{}\nedge label list : \t{}\nedge vertex list : \t{}\n'.format(\
                str(self.size),\
                ' '.join(map(formatEdgeTuple, getGraphEdgeList(self.subgraph))),\
                ' '.join(map(formatEdgeTuple, getGraphEdgeLabelList(self.subgraph))))
    def __rpr__(self):
        return self.__str__()
    
    def getCsvHeader():        
        return 'length ;edge label list; edge vertex list\n'
        
    def getCsv(self):
        return '{};{};{}\n'.format(\
                str(self.size),\
                ' '.join(map(formatEdgeTuple, getGraphEdgeList(self.subgraph))),\
                ' '.join(map(formatEdgeTuple, getGraphEdgeLabelList(self.subgraph))))


def generateTdsPathConstraint(pattern, pathConstraintList):
    tdsPathConstraintDict={}
    
    for pathConstraint in pathConstraintList:
        if not pathConstraint.initialLabel in tdsPathConstraintDict:
            tdsPathConstraintDict[pathConstraint.initialLabel]=\
                TdsPathConstraint(pathConstraint.getSubgraph(pattern),False)
        else:
            tdsPathConstraintDict[pathConstraint.initialLabel]=\
                TdsPathConstraint(graphUnion(tdsPathConstraintDict[pathConstraint.initialLabel].subgraph,\
                           pathConstraint.getSubgraph(pattern)), True)
                
    tdsPathConstraintList=[]
    for label in tdsPathConstraintDict:
        if tdsPathConstraintDict[label].fromMerge:
            tdsPathConstraintList.append(tdsPathConstraintDict[label])
            
    
    return tdsPathConstraintList

def writeTdsPathConstraint(outputResultDirectory, tdsPathConstraintList):
    outputResultTdsPathConstraint=outputResultDirectory + 'tds_path_constraint.txt'
    with open(outputResultTdsPathConstraint, 'w') as file:
        file.write(TdsPathConstraint.getCsvHeader())
        for tdsPathConstraint in tdsPathConstraintList:
            file.write(tdsPathConstraint.getCsv())
    file.close()   
    