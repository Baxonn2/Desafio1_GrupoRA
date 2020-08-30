from copy import deepcopy as copy
import heapq


class State:
	pl = 0		   # largo de las tablas
	dims = []      # lista de dimensiones por cortar
	planks = []    # lista de tabla (dimensión) restante por palo
	cuts = []      # lista de cortes por palo [[100, 300, 400], [3000, 200], [500, 2700]]
	visited = False
	bf = 0         # heuristica best fit: cada tabla que no tenga dimensión restante
				   # 					  suma 1 punto, de esta forma se minimiza el 
				   #					  gasto por tabla, (mejor bf, mejor estado)
	ub = 0		   #upper bound

	def __init__(self,dims,planks_length):
		self.dims=dims
		self.planks=[]
		self.cuts = []
		self.visited=False
		self.pl=planks_length
		self.bf=0
		self.ub=len(dims)

		# todas las dimensiones mayores al largo de la plank serán truncadas
		for i in self.dims:
			if i > self.pl:
				self.dims.pop(self.dims.index(i))
				self.dims.append(self.pl)

		total_dim = 0
		for i in self.dims:
			total_dim+=i

		#set el lower bound. La cantidad mínima de tablas es la suma de las dimensiones / largo tabla
		while total_dim>0:
			self.planks.append(planks_length)
			total_dim-=planks_length

		for i, a in enumerate(self.planks):
			self.cuts.append([])


	# se define el operador '<' para los estados, donde un operador con mayor numero de best fits 
	# será menor que otro con menor número, está al revés por temas de la cola con prioridad, 
	# mayor bf, mayor prioridad
	def __lt__(self, other):
		if len(self.planks) != len(other.planks):
			return len(self.planks) > len(other.planks)

		if self.bf != other.bf:
			return self.bf > other.bf

		return wf(self) < wf(other)

# heuristica de menor porcentaje de desperdicios
def wf(state):
	w = 0
	for i in state.planks:
		sobra = (i/state.pl)*100
		w+= sobra**3 
	return w/10000



class Action:
	cut = 0      #dimensión a cortar
	plank = 0    #tabla a la cual cortarle la dimensión 

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

	if len(actions)> 0:
		return actions
	else:				# si no hay acciones validas se agrega una tabla
		state.planks.append(state.pl)
		state.cuts.append([])
		if(len(state.planks)<state.ub):	# previene loop infinito
			return get_actions(state)
		else: 
			return []


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
	# si la acción hizo un perfect fit (largo restante = 0 )
	if new_state.planks[action.plank] == 0:
		new_state.bf+=1

	return new_state

def visit(state):
	state.visited=True

def visited(state):
	return state.visited

def best_first(state: State):
	q = []
	itera = 0
	heapq.heappush(q,state)
	while len(q) >0:
		itera+=1
		node = heapq.heappop(q)
		if visited(node):
			continue
		else:
			visit(node)

		if is_final_state(node):
			print ('iteraciones: {}   tablas: {}'.format(itera,len(node.planks)))
			return node

		actions=get_actions(node)
		for action in actions:
			sub_node = transition(node,action) 
			if not visited(sub_node):
				heapq.heappush(q,sub_node)


state = State([100,200,32200,400,500,3000,2700,1601,1601,1601,1599,1601,1601,1601,1601,1601,1601],3200)

best = best_first(state)

print(best.cuts)


