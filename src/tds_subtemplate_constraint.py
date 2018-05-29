#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 02:24:51 2018

@author: qiu
"""

def getGraphEdgeList(graph):
    return graph.edges

def getGraphEdgeLabelList(graph):
    graphEdgeList=[]
    for edge in graph.edges:
        vertex1, vertex2=edge
        graphEdgeList.append((graph.nodes[vertex1]['label'], graph.nodes[vertex2]['label']))
    return graphEdgeList

def formatEdgeTuple(edgeTuple):
    return '('+str(edgeTuple[0])+','+str(edgeTuple[1])+')'

class TdsSubtemplateConstraint():
    def __init__(self, subgraph):
        
        self.size=subgraph.number_of_nodes()
        self.subgraph=subgraph
                
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

def generateTdsSubtemplateConstraint(pattern):
    return [TdsSubtemplateConstraint(pattern)]
    
def writeTdsSubtemplatecConstraint(outputResultDirectory, tdsSubtemplateConstraintList):
    outputResultTdsSubtemplateConstraint=outputResultDirectory + 'tds_subtemplate_constraint.txt'
    with open(outputResultTdsSubtemplateConstraint, 'w') as file:
        file.write(TdsSubtemplateConstraint.getCsvHeader())
        for tdsSubtemplateConstraint in tdsSubtemplateConstraintList:
            file.write(tdsSubtemplateConstraint.getCsv())
    file.close()   
