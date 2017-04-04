# Branch and bound implementation for TSP

import copy
import Queue
import numpy as np

# Calculates total path distance of the edges connecting the nodes in nodes_visited according to the graph adjacency matrix.
def calculate_path_distance(graph, nodes_visited):
	distance = 0
	for i in range(1, len(nodes_visited)):
		distance = distance + graph[nodes_visited[i-1], nodes_visited[i]]
	return distance

# Bounding function: reduced cost matrix
# Input:
# - current_lower_bound: cost lower bound of current_graph
# - input_graph: original graph (unused)
# - current_graph: adjacency matrix
# - steps: nodes visited in order (unused)
# Returns (cost lower bound, reduced adjacency matrix (cloned))
def reduced_cost_matrix(current_lower_bound, input_graph, current_graph, steps):
	row, col = current_graph.shape
	output_graph = current_graph.copy()

	# Reduce rows
	for r in range(0, row):
		min_distance = -1
		for c in range(0, col):
			if min_distance < 0 or (output_graph[r, c] >= 0 and output_graph[r, c] < min_distance):
				min_distance = output_graph[r, c]
		if min_distance >= 0:
			for c in range(0, col):
				if output_graph[r, c] >= 0:
					output_graph[r, c] = output_graph[r, c] - min_distance
			current_lower_bound = current_lower_bound + min_distance

	# Reduce cols
	for c in range(0, col):
		min_distance = -1
		for r in range(0, row):
			if min_distance < 0 or (output_graph[r, c] >= 0 and output_graph[r, c] < min_distance):
				min_distance = output_graph[r, c]
		if min_distance >= 0:
			for r in range(0, row):
				if output_graph[r, c] >= 0:
					output_graph[r, c] = output_graph[r, c] - min_distance
			current_lower_bound = current_lower_bound + min_distance

	return (current_lower_bound, output_graph)

# Bounding function: complete tour cost
# Input:
# - current_lower_bound: cost lower bound of current_graph (unused)
# - input_graph: original graph
# - current_graph: adjacency matrix
# - steps: nodes visited in order
# Returns (cost lower bound, complete tour cost (cloned))
def complete_tour_cost(current_lower_bound, input_graph, current_graph, steps):
	visited_distance = calculate_path_distance(input_graph, steps)
	row, col = current_graph.shape
	cost = 0
	minimum_outgoing_edges = []

	# Calculate the lower bound of the cost of unvisited nodes - outgoing edges
	for r in range(0, row):
		min_distance = -1
		min_c = None
		for c in range(0, col):
			if min_distance < 0 or (current_graph[r, c] >= 0 and current_graph[r, c] < min_distance):
				min_distance = current_graph[r, c]
				min_c = c
		if min_distance >= 0:
			cost = cost + min_distance
			minimum_outgoing_edges.append((r, min_c))

	# Calculate the lower bound of the cost of unvisited nodes - incoming edges
	for c in range(0, col):
		min_distance = -1
		for r in range(0, row):
			if (c, r) not in minimum_outgoing_edges:
				if min_distance < 0 or (current_graph[r, c] >= 0 and current_graph[r, c] < min_distance):
					min_distance = current_graph[r, c]
		if min_distance >= 0:
			cost = cost + min_distance

	output_graph = current_graph.copy()
	return (visited_distance + (cost/2), output_graph)

# Calculates TSP solution using branch-and-bound.
# Input:
# - input_graph: n x n adjacency matrix (NumPy matrix), with infinite distances represented by negative numbers.
# - bounding_function: reduced_cost_matrix or complete_tour_cost
# Returns a tuple of (shortest cycle distance, nodes visited in order)
def tsp_branch_and_bound(input_graph, bounding_function):

	graph_n = input_graph.shape[0]
	pq = Queue.PriorityQueue()
	insert_index = 0 # Unique insertion order index for each priority queue item, needed for proper sorting in case two items' lower bounds are equal
	start_lower_bound, start_graph = bounding_function(0, input_graph, input_graph, [0])
	pq.put((start_lower_bound, 0, start_graph, [0]))
	best_solution = (None, [])

	while not pq.empty():
		current_lower_bound, current_insert_index, current_graph, steps = pq.get()

		# DEBUG
		print current_lower_bound, steps

		# Stop if the current lower bound is greater than the solution's cycle distance
		if best_solution[0] is not None and current_lower_bound >= best_solution[0]:
			break

		# Found a possible solution
		if len(steps) == graph_n and input_graph[steps[-1], 0] >= 0:
			steps.append(0)
			cycle_distance = calculate_path_distance(input_graph, steps)
			if best_solution[0] is None or cycle_distance < best_solution[0]:
				best_solution = (cycle_distance, steps)
			continue

		# Visit next nodes
		for next_node in range(0, graph_n):
			if current_graph[steps[-1], next_node] >= 0:
				next_graph = current_graph.copy()
				for i in range(0, graph_n):
					next_graph[steps[-1], i] = -1
					next_graph[i, next_node] = -1
				next_graph[next_node, steps[-1]] = -1
				next_steps = copy.deepcopy(steps)
				next_steps.append(next_node)
				next_lower_bound, next_graph = bounding_function(current_lower_bound, input_graph, next_graph, next_steps)
				insert_index = insert_index + 1
				pq.put((next_lower_bound, insert_index, next_graph, next_steps))

	return best_solution
