#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 00:18:29 2018

@author: qiu
"""
from collections import *

class CircleConstraint():
    def __init__(self, labelList, vertexList):
        # Remove the last vector which is the same as the first one
        self.size=len(vertexList)-1        
        
        # Re-order the vertex list such as :
        #  + vertexList[0] is the minimal vertex index
        #  + vertexList[1]<vertexList[-1]
        # This is used to test equality between constraint
        minVertex=min(vertexList)
        minVertexIndex=vertexList.index(minVertex)
        
        previousIndex=minVertexIndex-1
        nextIndex=minVertexIndex+1
        if previousIndex<0:
            previousIndex=self.size-1
        if nextIndex>self.size-1:
            nextIndex=0
            
        reverse=(vertexList[previousIndex]<vertexList[nextIndex])
        
        self.labelList=[0]*self.size
        self.vertexList=[0]*self.size     
        originalIndex=minVertexIndex
        for currentIndex in range(self.size):
            self.labelList[currentIndex]=labelList[originalIndex]
            self.vertexList[currentIndex]=vertexList[originalIndex]
            
            if reverse:
                originalIndex-=1
            else:
                originalIndex+=1
            
            if originalIndex>self.size-1:
                originalIndex=0
            elif originalIndex<0:
                originalIndex=self.size-1
                
    def getSubgraph(self, pattern):
        return  pattern.subgraph(self.vertexList)
                
    def __eq__(self, other):
        return self.size==other.size and self.vertexList==other.vertexList
    def __ne__(self, other):
        return not __eq__(self, other)
    def __hash__(self):
        return hash(self.vertexList)
    
    
    def __str__(self):
        return 'length : \t{}\nlabel list : \t{}\nvertex list : \t{}\n'.format(\
                str(self.size),\
                ' '.join(map(str, self.labelList)), ' '.join(map(str, self.vertexList)))
    def __rpr__(self):
        return self.__str__()
    
    def getCsvHeader():        
        return 'length ;label list; vertex list\n'
        
    def getCsv(self):
        return '{};{};{}\n'.format(\
                str(self.size),\
                ' '.join(map(str, self.labelList)), ' '.join(map(str, self.vertexList)))
    
def runCircleConstraintSearch(pattern, circleConstraintList, originalVertex, \
                              currentVertex, historyLabelList, historyVertexList, currentDepth):
    if currentDepth>pattern.number_of_nodes():
        return
    
    if currentDepth>=3 and originalVertex==currentVertex:
        circleConstraint = CircleConstraint(historyLabelList, historyVertexList)
        
        if not (circleConstraint in circleConstraintList):
            circleConstraintList.append(circleConstraint)
            
        return
    
    for neighborVertex in pattern.neighbors(currentVertex):
        # Avoid back-tracking but leaves the possibility to go back to the initial vertex
        if neighborVertex in historyVertexList[1:]: 
            continue
        
        neighborLabel=pattern.nodes[neighborVertex]['label']
        
        historyVertexList.append(neighborVertex)
        historyLabelList.append(neighborLabel)
        
        runCircleConstraintSearch(pattern, circleConstraintList, originalVertex, \
                                  neighborVertex, historyLabelList, historyVertexList, currentDepth+1)
        
        historyVertexList.pop()
        historyLabelList.pop()
    
    
    
def generateCircleConstraint(pattern):
    circleConstraintList=[]
    
    for vertex in pattern.node():
        label=pattern.nodes[vertex]['label']
        
        historyLabelList=[label]
        historyVertexList=[vertex]
        
        runCircleConstraintSearch(pattern, circleConstraintList, vertex, \
                                  vertex, historyLabelList, historyVertexList, 0)
        
    return circleConstraintList

def writeCircleConstraint(outputResultDirectory, circleConstraintList):
    outputResultCircleConstraint=outputResultDirectory + 'circle_constraint.txt'
    with open(outputResultCircleConstraint, 'w') as file:
        file.write(CircleConstraint.getCsvHeader())
        for circleConstraint in circleConstraintList:
            file.write(circleConstraint.getCsv())
    file.close()
    