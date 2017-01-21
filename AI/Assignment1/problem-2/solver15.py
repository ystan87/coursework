# implements the sliding 15-puzzle
# input is a file containing a 4x4 matrix 
# with rows delimited by newlines and columns delimited by spaces
# the program first checks if there is a theoretically possible solution
# it will not attempt to find if there is none
# final line of output is the sequence of moves taken
# the value of heuristic is the sum over all tiles of the shortest number of moves to
# their position in the goal state
# the function solve() tries to find a solution with the consistent heuristic h()
# the heuristic given is consistent because each step decreases the heuristic by at most 1 and is o at the goal state
# therefore a graph-search would suffice and the solution will be optimal
from Queue import PriorityQueue as pq
from sets import Set
import copy
import sys

# specifies command line input format if proper parameters are not provided
if (len(sys.argv) < 2) :
    print 'Enter proper parameters.'
    print 'Usage: python solver15.py [filename]'
    exit()
    
# assign goal state
global goal_state, initial_state
goal_state = []
initial_state = []
for i in range(4):
	row = []
	for j in range(4):
		row.append(i*4 + j + 1)
		if i == 3 and j == 3:
			row[j] = 0		
	goal_state.append(row)
	
def readfile(input_filename):
	with open(input_filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			raw_row = line.split(' ')
			if len(raw_row) != 4:
				raise ValueError("Number of columns should be 4")
			row = [int(x) for x in raw_row]
			initial_state.append(row)
		if len(initial_state)!= 4:
			raise ValueError("Number of rows should be 4")
	
# diagnostic function
def print_state(state):
	for i in range(len(state)):
		print state[i]
		
# for producing immutable copies of states
def collapse(state):
	collapsed = []
	for row in state:
		for element in row:
			collapsed.append(element)
	return tuple(collapsed)
	
# convert tile numbers into its zero-based coordinate
def convert(tile):
	if tile == 0:
		return None
	else:
		tile -= 1
		return [tile/4, tile%4]
		
# get the position of the empty tile
def get_empty_position(state):
	for i in range(4):
		for j in range(4):
			if state[i][j] == 0:
				return [i, j]
				
def difference(a, b):
	d = a - b
	if d%2 == 1:
		return 1
	elif d%4 == 0:
		return 0
	else:
		return 2
		
def increment(a):
	a += 1
	if a == 4:
		a = 0
	return a
	
def decrement(a):
	a -= 1
	if a == -1:
		a = 3
	return a
		
# the distance of a tile from its position in the goal state
def distance(tile, position):
	dx = difference(tile[0], position[0])
	dy = difference(tile[1], position[1])
	return dx + dy

# the heuristic function
def h(state):
	heuristic = 0
	for i in range(4):
		for j in range(4):
			position = [i, j]
			tile = convert(state[i][j])
			if tile is None:
				continue
			heuristic += distance(tile, position)
	return heuristic
	
# moves the board in state according as specified by step
def move(step, state):
	empty = get_empty_position(state)
	new_state = copy.deepcopy(state)
	if step == 'U':
		new_empty = [increment(empty[0]), empty[1]]
		new_state[empty[0]][empty[1]] = state[new_empty[0]][new_empty[1]]
		new_state[new_empty[0]][new_empty[1]] = 0
	elif step == 'D':
		new_empty = [decrement(empty[0]), empty[1]]
		new_state[empty[0]][empty[1]] = state[new_empty[0]][new_empty[1]]
		new_state[new_empty[0]][new_empty[1]] = 0
	elif step == 'L':
		new_empty = [empty[0], increment(empty[1])]
		new_state[empty[0]][empty[1]] = state[new_empty[0]][new_empty[1]]
		new_state[new_empty[0]][new_empty[1]] = 0
	elif step == 'R':
		new_empty = [empty[0], decrement(empty[1])]
		new_state[empty[0]][empty[1]] = state[new_empty[0]][new_empty[1]]
		new_state[new_empty[0]][new_empty[1]] = 0
	else:
		pass
		
	return new_state
		
# generates list of successors and the steps taken
def successors(state):
	next = []
	for step in list("UDLR"):
		current_state = state
		next.append([move(step, current_state), step])
	return next
		
# Number of permutation inversions
def num_perm_inv(l):
	perm_inv= 0
	for i in range(1,len(l)) :
		for j in range(len(l)):
			if l[j] > i:
				perm_inv += 1
			elif l[j] == i:
				break
			else:
				continue
	return perm_inv
				
# Is it actually solvable?
def is_solvable(state):
	l = list(collapse(state))
	e = get_empty_position(state)
	if e[0]%2 == num_perm_inv(l)%2 :
		return False
	return True
	
# solves the 15-puzzle purely with heuristic h()
def solve():
	print "The initial state is:"
	print_state(initial_state)
	if not is_solvable(initial_state):
		print "There is no solution. Any attempt would be futile."
		return None
	state = initial_state
	number_steps = 0
	min_heuristic = h(state)
	print "The starting heuristic is {}".format(min_heuristic)
	if initial_state == goal_state:
		print "Completed in {} steps".format(number_steps)
		return []
	fringe = pq()
	fringe.put((number_steps + h(state), state))
	predecessor = {collapse(initial_state): [None, None, 0]}
	explored = Set()
	explored.add(collapse(initial_state))
	while not fringe.empty():
		state = fringe.get()[1]
		y, z, number_steps_next = predecessor[collapse(state)]
		number_steps_next += 1
		for next_state, step in successors(state):
			if next_state == goal_state:
				solution_path = [step]
				prev_state = state
				while prev_state != initial_state:
					step, prev_state, u = predecessor[collapse(prev_state)]
					solution_path.insert(0, step)
				print "Goal reached!"
				print_state(next_state)
				print "A solution is found with depth {} steps".format(number_steps_next)
				print "Size of explored states is {}".format(len(explored))
				return solution_path
				
			if collapse(next_state) not in explored:
				# diagnostics
				#if h(next_state) < min_heuristic:
					#min_heuristic = h(next_state)
					#print "The minimum heuristic reached is {}".format(min_heuristic)
				if len(explored) % 1000000 == 0:
					print "Number of million steps explored is {}".format(len(explored) / 1000000)
				explored.add(collapse(next_state))
				fringe.put((number_steps_next + h(next_state), next_state))
				predecessor[collapse(next_state)] = [step, state, number_steps_next]

# prints the solution
def print_solution():
	solution_path = solve()
	if solution_path is None:
		return
	solution_string = ""
	for step in solution_path:
		solution_string += step + " "
	print "The solution found is as follows:"
	print solution_string

readfile(sys.argv[1])
print_solution()
