#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 20:55:34 2018

@author: qiu
"""
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import networkx as nx
from collections import *

import utils
import local_constraint
import circle_constraint
import path_constraint
import tds_cyclic_constraint
import tds_path_constraint
import tds_subtemplate_constraint

def main(inputPatternEdges, inputPatternVertexData, outputResultDirectory):
    pattern=utils.readPatternEdges(inputPatternEdges)
    utils.readPatternVertexData(pattern, inputPatternVertexData)
    
    # Generate local constraint
    localConstraintList=local_constraint.generateLocalConstraint(pattern)
    local_constraint.writeLocalConstraint(outputResultDirectory, localConstraintList)
    
    # Find leaf with unique label and prune the pattern
    leafVertexWithUniqueLabelList=utils.findLeafVertexWithUniqueLabel(pattern)
    pattern.remove_nodes_from(leafVertexWithUniqueLabelList)
    
    # Generate circle constraint
    circleConstraintList=circle_constraint.generateCircleConstraint(pattern)
    circle_constraint.writeCircleConstraint(outputResultDirectory, circleConstraintList)
    
    # Generate path constraint
    pathConstraintList=path_constraint.generatePathConstraint(pattern)
    path_constraint.writePathConstraint(outputResultDirectory, pathConstraintList)
    
    # Generate TDS edge monocyclic constraint
    tdsCyclicConstraintList=tds_cyclic_constraint.generateTdsCyclicConstraint(pattern, circleConstraintList)
    tds_cyclic_constraint.writeTdsCyclicConstraint(outputResultDirectory, tdsCyclicConstraintList)
    
    # Generate TDS path constraint
    tdsPathConstraintList=tds_path_constraint.generateTdsPathConstraint(pattern, pathConstraintList)
    tds_path_constraint.writeTdsPathConstraint(outputResultDirectory, tdsPathConstraintList)
    
    # Generate TDS partial constraint
    tdsSubtemplateConstraintList=tds_subtemplate_constraint.generateTdsSubtemplateConstraint(pattern)
    tds_subtemplate_constraint.writeTdsSubtemplatecConstraint(outputResultDirectory, tdsSubtemplateConstraintList)

# TEST
# TEST
main('data/test2/patterns/pattern_edge', \
     'data/test2/patterns/pattern_vertex_data', \
     'data/test2/results/')
main('data/test1/patterns/pattern_edge', \
     'data/test1/patterns/pattern_vertex_data', \
     'data/test1/results/')

if __name__ == '__main__':
    print('')