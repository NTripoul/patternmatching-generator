#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 02:00:08 2018

@author: qiu
"""
import networkx as nx
from collections import *


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

def isGraphIntersectionEmpty(graph1,graph2):    
    if graph1.number_of_edges()<=graph2.number_of_edges():
        for e in graph1.edges():
            if graph2.has_edge(*e):
                return False
    else:
        for e in graph2.edges():
            if graph1.has_edge(*e):
                return False

    return True

def graphUnion(graph1, graph2):
    union = graph1.fresh_copy()
    # add graph attributes, graph2 attributes take precedent over graph1 attributes
    union.graph.update(graph1.graph)
    union.graph.update(graph2.graph)

    union.add_nodes_from(graph1)
    union.add_edges_from(graph1.edges(data=True))
    
    union.add_nodes_from(graph2)
    union.add_edges_from(graph2.edges(data=True))
    
    for n in graph1:
        union.nodes[n].update(graph1.nodes[n])
    for n in graph2:
        union.nodes[n].update(graph2.nodes[n])

    return union

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

def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)

def writeTdsCyclicConstraint(outputResultDirectory, tdsCyclicConstraintList):
    outputResultTdsCyclicConstraint=outputResultDirectory + 'tds_cyclic_constraint.txt'
    with open(outputResultTdsCyclicConstraint, 'w') as file:
        file.write(TdsCyclicConstraint.getCsvHeader())
        for tdsCyclicConstraint in tdsCyclicConstraintList:
            file.write(tdsCyclicConstraint.getCsv())
    file.close()   
    