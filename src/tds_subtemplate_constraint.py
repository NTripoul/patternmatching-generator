#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from graphUtils import *

class TdsSubtemplateConstraint():
    def __init__(self, subgraph):
        
        self.size=subgraph.number_of_nodes()
        self.subgraph=subgraph
                
    def __str__(self):
        return 'length : \t{}\nedge label list : \t{}\nedge vertex list : \t{}\n'.format(\
                str(self.size),\
                ' '.join(map(formatEdgeTuple, getGraphEdgeLabelList(self.subgraph))),\
                ' '.join(map(formatEdgeTuple, getGraphEdgeList(self.subgraph))))
    def __rpr__(self):
        return self.__str__()
    
    def getCsvHeader():        
        return 'length ;edge label list; edge vertex list\n'
        
    def getCsv(self):
        return '{};{};{}\n'.format(\
                str(self.size),\
                ' '.join(map(formatEdgeTuple, getGraphEdgeLabelList(self.subgraph))),\
                ' '.join(map(formatEdgeTuple, getGraphEdgeList(self.subgraph))))

def generateTdsSubtemplateConstraint(pattern):
    return [TdsSubtemplateConstraint(pattern)]
    
def writeTdsSubtemplatecConstraint(outputResultDirectory, tdsSubtemplateConstraintList):
    outputResultTdsSubtemplateConstraint=outputResultDirectory + 'tds_subtemplate_constraint.txt'
    with open(outputResultTdsSubtemplateConstraint, 'w') as file:
        file.write(TdsSubtemplateConstraint.getCsvHeader())
        for tdsSubtemplateConstraint in tdsSubtemplateConstraintList:
            file.write(tdsSubtemplateConstraint.getCsv())
    file.close()   
