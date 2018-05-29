#!/bin/bash


echo 'Constraint generation - Test 1 - Start'
python src/main.py --input_pattern_edges data/test1/patterns/pattern_edge --input_pattern_data data/test1/patterns/pattern_vertex_data --output_directory data/test1/results/
echo 'Constraint generation - Test 1 - End'

echo 'Constraint generation - Test 2 - Start'
python src/main.py --input_pattern_edges data/test2/patterns/pattern_edge --input_pattern_data data/test2/patterns/pattern_vertex_data --output_directory data/test2/results/
echo 'Constraint generation - Test 2 - End'

