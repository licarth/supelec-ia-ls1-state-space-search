# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
from Crypto import Util

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class Node:
  nodeCount = 0
  def __init__(self, state, action, parent, cost):
    self.state = state
    self.action = action
    self.parent = parent
    self.cost = cost
    self.no = Node.nodeCount
    Node.nodeCount = Node.nodeCount + 1  

  def getCost(self):
    return self.cost
  
  def getState(self):
    return self.state
  
  def getAction(self):
    return self.action
  
  def getParent(self):
    return self.parent
  
  def getNumber(self):
    return self.no

  def getListOfActions(self):
    actions = []
    node = self
    while not node.getAction() == '':
      actions.append(node.getAction())
      node = node.getParent()
    actions.reverse()
    return actions
    
  def getSuccessors(self, problem):
    return list(map(lambda s: Node(s[0], s[1], self, s[2] + self.getCost()), 
                problem.getSuccessors(self.getState())))
    
  def __lt__(self, other):
    return self.cost < other.cost
  
class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
    """
    Returns the start state for the search problem
    """
    util.raiseNotDefined()

  def isGoalState(self, state):
    """
      state: Search state
    
    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def getSuccessors(self, state):
    """
      state: Search state
    
    For a given state, this should return a list of triples,
    (successor, action, stepCost), where 'successor' is a
    successor to the current state, 'action' is the action
    required to get there, and 'stepCost' is the incremental
    cost of expanding to that successor
    """
    util.raiseNotDefined()



  def getCostOfActions(self, actions):
    """
      actions: A list of actions to take
    
    This method returns the total cost of a particular sequence of actions.  The sequence must
    be composed of legal moves
    """
    util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print("Start:", problem.getStartState())
  print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
  print("Start's successors:", problem.getSuccessors(problem.getStartState()))
  """
  "*** YOUR CODE HERE ***"
  print(("Start:", problem.getStartState()))
  print(("Is the start a goal?", problem.isGoalState(problem.getStartState())))
  print(("Start's successors:", problem.getSuccessors(problem.getStartState())))

  start = (((0,0),'',0), (problem.getStartState(), '', 0)) # Beware: introducing [] action
  nopen = []
  nopen.append(start)
  nclosed = {}  
  while nopen:
    (parent, current) = nopen.pop()
    nclosed[current[0]] = (parent[0], parent[1]) # On ajoute le noeud à l'ensemble des noeuds explorés.
    if problem.isGoalState(current[0]) : # current[0] is state
        return solution(problem, start[1], current, nclosed)
    # return (map (lambda ((parent, current)): current[1], nclosed))
    for s in problem.getSuccessors(current[0]):
        if s[0] not in nclosed:
            nopen.append((current, s))
  return []

def solutionNew(problem, start, node, listn):
    actions = []
    while not node.getstate() == start.getState():
      actions.append(node.getAction())
      node = node.getParent()
    actions.reverse()
    return actions
  
def solution(problem, start, node, listn):
    actions = []
    c = (node[0], node[1])
    while not c[0] == start[0]:
        actions.append(c[1])
        c = listn[c[0]]
    actions.reverse()
    return actions
  
def looping(node):
  parent = node.getParent()
  while (parent):
    if (parent.getState() == node.getState()):
      return True
    parent = parent.getParent()
  return False

def enqueueNodesWithoutCycles(queue, newNodes):
  return list(map(
                  queue.push,
                   filter(lambda n: not looping(n), newNodes)
                   )) #filter() filtre les éléments qui vérifient la fonction donnée
  
def generalSearch(problem, openNodes, queuingFn):
  """
  """
  start = Node(problem.getStartState(), '', '', 0)
  openNodes.push(start)
  while openNodes:
    current = openNodes.pop()
    if problem.isGoalState(current.getState()):
      return current.getListOfActions()
    queuingFn(openNodes, current.getSuccessors(problem))
  
def depthFirstSearchNew(problem):
  return generalSearch(problem, util.Stack(), enqueueNodesWithoutCycles)
      
def breadthFirstSearchNew(problem):
  table = {}
  
  def register(q, n):
    table[n.getState()] = n
    q.push(n)
    
  def enqueueNodesWithourDuplicates(queue, newNodes):
    list(map(lambda n: register(queue, n), filter(lambda n: n.getState() not in table, newNodes)))
  
  return generalSearch(problem, util.Queue(), enqueueNodesWithourDuplicates)
  
def breadthFirstSearch(problem):
  from collections import deque
  "Search the shallowest nodes in the search tree first. [p 81]"
  start = (((0,0),'',0), (problem.getStartState(), '', 0)) # Beware: introducing [] action
  nopen = deque([])
  nopen.append(start)
  nclosed = {}
  while nopen:
    (parent, current) = nopen.popleft()
    nclosed[current[0]] = (parent[0], parent[1]) # On ajoute le noeud à l'ensemble des noeuds explorés.
    if problem.isGoalState(current[0]) : # current[0] is state
        return solution(problem, start[1], current, nclosed)
    # return (map (lambda ((parent, current)): current[1], nclosed))
    for s in problem.getSuccessors(current[0]):
        if s[0] not in nclosed:
            nopen.append((current, s))
  return []
#   util.raiseNotDefined()

def uniformCostSearchNew(problem):
  table = {}
  
  def register(q, n):
    table[n.getState()] = n
    q.push(n)
    
  def enqueueNodesWithoutDuplicates(queue, newNodes):
    list(map(lambda n: register(queue, n), filter(lambda n: n.getState() not in table, newNodes)))
  
  return generalSearch(problem, util.PriorityQueueWithFunction(lambda n: n.getCost()), enqueueNodesWithoutDuplicates)
  
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  from util import PriorityQueue
  "Search the shallowest nodes in the search tree first. [p 81]"
  start = (((0,0),'',0), (problem.getStartState(), '', 0)) # Beware: introducing [] action
  nopen = PriorityQueue()
  nopen.push(start, 0)
  nclosed = {} #Noeuds explorés.
  while nopen:
    (parent, current) = nopen.pop()
    nclosed[current[0]] = (parent[0], parent[1]) # On ajoute le noeud à l'ensemble des noeuds explorés.
    if problem.isGoalState(current[0]) : # current[0] is state
        return solution(problem, start[1], current, nclosed)
    # return (map (lambda ((parent, current)): current[1], nclosed))
    for s in problem.getSuccessors(current[0]):
        if s[0] not in nclosed:
            nopen.push((current, s),current[2])
#         else:
#           if (s[0] in nopen):
#             if (nopen[s[0]][2] > s[2]):
#             nopen
  return []

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearchNew
dfs = depthFirstSearchNew
astar = aStarSearch
ucs = uniformCostSearchNew
