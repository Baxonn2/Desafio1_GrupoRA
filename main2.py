from copy import deepcopy as copy
from queue import PriorityQueue



class State:
	pl = 0
	dims = []      # lista de dimensiones por cortar
	planks = []    # lista de palo restante por palo
	cuts = []      # lista de cortes por palo
	visited = False
	bf = 0

	def __init__(self,dims,planks_length):
		self.dims=dims
		self.planks=[]
		self.cuts = []
		self.visited=False
		self.pl=planks_length
		self.bf=0

		total_dim = 0
		for i in self.dims:
			total_dim+=i

		while total_dim>0:
			self.planks.append(planks_length)
			total_dim-=planks_length

		for i, a in enumerate(self.planks):
			self.cuts.append([])

	def sort_cuts(self):
		self.cuts.sort()
		# sort by valor total maybe?ol{+`9}
		for i in self.cuts:
			i.sort()

	def __lt__(self, other):
		selfPriority = self.bf
		otherPriority = other.bf
		return selfPriority < otherPriority


class Action:
	cut = 0
	plank = 0

	def __init__(self,plank,cut):
		self.cut=cut
		self.plank=plank

def get_actions(state: State):
	actions = []
	for dim in state.dims:
		for plank, a in enumerate(state.planks):
			action = Action(plank, dim)
			if is_state_valid(transition(state,action)):
				actions.append(action)
	return actions


def is_state_valid(state: State):
	for plank in state.planks:
		if plank<0 :
			return False

	return True

def is_final_state(state: State):
	if len(state.dims)==0:
		return True
	else:
		return False

def transition(state: State, action: Action):
	new_state = copy(state)
	new_state.visited = False
	new_state.planks[action.plank]-=action.cut
	new_state.cuts[action.plank].append(action.cut)
	new_state.dims.remove(action.cut)
	#print(new_state.planks)
	return new_state

def visit(state):
	state.visited=True

def visited(state):
	return state.visited

def best_fit(state):
	best_fits = 0
	for i in state.planks:
		if i == 0:
			best_fits+=1
	state.bf=best_fits
	return int(best_fits)



def not_in_by_content(solutions,node):
	for i in solutions:
		if i.cuts == node.cuts:
			return False #revisar si las tablas están ordenadas también
	return True

def DFS(state: State):
	solutions = []
	stack = []
	state.visited=False
	stack.append(state)

	while(len(stack) > 0):
		node = stack.pop()

		if visited(node):
			continue
		else:
			visit(node)

		if is_final_state(node):
			return node

		actions=get_actions(node)
		for action in actions:
			sub_node = transition(node,action) 
			if not visited(sub_node):
				stack.append(sub_node)


	return solutions

def best_first(state: State):
	q = PriorityQueue()
	q.put( (4,state) )
	while not q.empty():
		pr , node = q.get()
		if visited(node):
			continue
		else:
			visit(node)

		if is_final_state(node):
			return node

		actions=get_actions(node)
		for action in actions:
			sub_node = transition(node,action) 
			if not visited(sub_node):
				q.put((-best_fit(sub_node),sub_node))



state = State([100,200,300,400,500,3000,2700],3200)
#get_actions(state)
#print(state.planks)
print(DFS(state).cuts)
#print(best_first(state).cuts)
#print(DFS(state).cuts)

