#!/usr/bin/env/python

# Travelling Salesperson Problem Solver
# 13515001 (K01) - Jonathan Christopher
# IF2211 Strategi Algoritma
# Algorithm: branch and bound
#  
# Input file format:
# <integer adjancency matrix of graph, negative numbers denote infinite distance>
# 
# Starts from the first vertex.
# Python 2.7 only.
# Usage: tsp-bb <input file>
# 
# Third-party libraries used:
# - NumPy: for efficient array/matrix operations (http://www.numpy.org, NumPy License)
# - Graphviz: for drawing graphs (http://www.graphviz.org, Eclipse Public License v1.0)

import time
import sys
import numpy as np
from graphviz import Digraph
import branchandbound as bb

# Main program
if __name__ == "__main__":

  print 'Travelling Salesman Problem Solver'
  print '13515001 (K01) - Jonathan Christopher'
  print 'IF2211 Strategi Algoritma'
  print '-------------------------------------'
  print ''

  # Process command-line arguments to get the input file
  if len(sys.argv) > 3 or len(sys.argv) == 2 and (sys.argv[1] == '--help' or sys.argv[1] == '-h' or sys.argv[1] == '/?'):
    print 'Usage: tsp-bb <input filename> [--reduced-cost-matrix|--complete-tour-cost]'
    exit(1)
  input_from_stdin = False
  if len(sys.argv) < 2 or sys.argv[1] == '-':
    fin = sys.stdin
    input_from_stdin = True
  else:
    fin = open(sys.argv[1], 'r')
  bounding_function = bb.reduced_cost_matrix
  if len(sys.argv) >= 3:
    if sys.argv[2] == '--complete-tour-cost':
      bounding_function = bb.complete_tour_cost

  # Read input from file or standard input
  if input_from_stdin:
    print 'Input n x n graph adjacency matrix (infinity: -1):'
  else:
    print 'Reading input graph from file...'
  input_graph_raw = []
  for line in fin:
    input_graph_raw.append([int(inp) for inp in line.split()])
  input_graph = np.matrix(input_graph_raw)

  # Verify whether input size is valid
  input_rows, input_cols = input_graph.shape
  if input_rows != input_cols:
    print 'Invalid input - adjacency matrix column count must be equal to its row count'
    exit(1)
  vertex_count = input_rows

  # Start of solver code
  if bounding_function == bb.reduced_cost_matrix:
    print 'Using reduced cost matrix bounding function:'
  elif bounding_function == bb.complete_tour_cost:
    print 'Using complete tour cost bounding function'
  print 'Starting solver...'
  start_time = time.time()

  shortest_cycle_distance, solution_nodes, nodes_generated, nodes_visited = bb.tsp_branch_and_bound(input_graph, bounding_function)

  # End of solver code
  end_time = time.time()
  print ''
  print 'Shortest cycle distance:', shortest_cycle_distance
  print 'Path:', map(lambda x: x+1, solution_nodes)
  print 'Nodes generated:', nodes_generated
  print 'Nodes visited:', nodes_visited
  print 'Execution time:', end_time - start_time, 'seconds.'

  # Generate result graph
  gv_output_graph = Digraph('Result graph', format='png', filename='result', engine='circo')
  for v in range(0, vertex_count):
    gv_output_graph.node(str(v+1), shape='circle')
  for r in range(0, vertex_count):
    for c in range(0, vertex_count):
      if input_graph[r, c] >= 0:
        edge_color = 'black'
        for i in range(1, len(solution_nodes)):
          if r == solution_nodes[i-1] and c == solution_nodes[i]:
            edge_color = 'red'
        gv_output_graph.edge(str(r+1), str(c+1), label=str(input_graph[r, c]), color=edge_color)

  # Output and show result graph (file: result.png)
  gv_output_graph.view()
