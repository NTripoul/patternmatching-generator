#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 02:00:08 2018

@author: qiu
"""
from collections import *
from graphUtils import *

def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)

class TdsCyclicConstraint():
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

def generateTdsCyclicConstraint(pattern, circleConstraintList):
    tdsCyclicConstraintDeque=deque([TdsCyclicConstraint(circleConstraint.getSubgraph(pattern), False)\
                                    for circleConstraint in circleConstraintList])
    
    currentIndex=0
    while currentIndex!= len(tdsCyclicConstraintDeque):
        nextIndex=currentIndex+1
        while nextIndex!= len(tdsCyclicConstraintDeque):
            if not isGraphIntersectionEmpty(tdsCyclicConstraintDeque[currentIndex].subgraph,\
                                         tdsCyclicConstraintDeque[nextIndex].subgraph):
                mergedSubgraph=graphUnion(tdsCyclicConstraintDeque[currentIndex].subgraph,\
                                            tdsCyclicConstraintDeque[nextIndex].subgraph)
                delete_nth(tdsCyclicConstraintDeque, nextIndex)
                delete_nth(tdsCyclicConstraintDeque, currentIndex)
                tdsCyclicConstraintDeque.appendleft(TdsCyclicConstraint(mergedSubgraph, True))
                break
            nextIndex+=1   
        else:
            currentIndex+=1
    
    currentIndex=0
    while currentIndex!= len(tdsCyclicConstraintDeque):
        if not tdsCyclicConstraintDeque[currentIndex].fromMerge:
            delete_nth(tdsCyclicConstraintDeque, currentIndex)            
        else:
            currentIndex+=1
    
    return list(tdsCyclicConstraintDeque)

def writeTdsCyclicConstraint(outputResultDirectory, tdsCyclicConstraintList):
    outputResultTdsCyclicConstraint=outputResultDirectory + 'tds_cyclic_constraint.txt'
    with open(outputResultTdsCyclicConstraint, 'w') as file:
        file.write(TdsCyclicConstraint.getCsvHeader())
        for tdsCyclicConstraint in tdsCyclicConstraintList:
            file.write(tdsCyclicConstraint.getCsv())
    file.close()   
    