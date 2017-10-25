import networkx as nx
import random as rand

import simconfig as config
import simdefaults as defaults

####################################################################################
# Converts a numerator and a denominator into a percentage.                        #
####################################################################################
def percent(numerator, denominator):
   return 100 * numerator / float(denominator)
####################################################################################



####################################################################################
# Gets a percentage of flagged nodes on the graph handed into it.                  #
# nodes that were flagged.                                                         #
'''
    Args:
        graph: A graph of our simulation
        num_flagged: The number of flagged nodes
    Returns:
        A percentage of nodes which are flagged (0% - 100%)

'''
####################################################################################
def percent_flagged(graph, num_flagged):
   return 100 * num_flagged / float(len(graph.node))
####################################################################################



####################################################################################
# Returns the total percentage of success given a graph, the number of flagged     #
# nodes and the total number of simulations.                                       #
####################################################################################
def total_percent_flagged(graph, num_flagged, num_simulations):
   return 100 * num_flagged / float((len(graph.node) * num_simulations))
####################################################################################



####################################################################################
# Pass in a graph, get the integer maximum weight of all edges                     #
####################################################################################
def max_weight(graph):
   max_weight = float('-inf')
   dict = nx.get_edge_attributes(graph, 'weight')
   for val in dict:
      max_weight = max(max_weight, dict[val])
   return max_weight
####################################################################################



####################################################################################
# Given a percentage chance (0.0 - 1.0), roll for that chance.                     #
####################################################################################
def chance(percentage_chance):
   if (percentage_chance > 1):
      print 'Percentage chance should never be MORE than 1. Even if you want 100% rolls.'
      return True
   if (percentage_chance <= 0):
      print 'Percentage chance being less than or equal to 0 will always reslult in a failure.' 
      return False
   if (rand.random() <= percentage_chance):
      return True
####################################################################################



####################################################################################
# Dumps information about the given graph.                                         #
####################################################################################
def output_graph_information(graph):
   print '*' * config.defaults.asterisk_space_count
   print 'Graph has ' + str(graph.number_of_nodes()) + ' node(s) and ' + str(graph.number_of_edges()) + ' edge(s).'
   print 'Density: ' + str(nx.density(graph))
   print 'Max weight of edges: ' + str(max_weight(graph))
   if nx.is_connected(graph):
      print 'Graph is completely connected.'
   else:
      print 'Graph is disjoint.'
   #print 'Betweenness centrality: ' + str(nx.betweenness_centrality(graph)) # It can be done!
   print '*' * config.defaults.asterisk_space_count
####################################################################################



####################################################################################
# Creates an attribute with an initial value.                                      #
####################################################################################
def create_node_attribute(graph, attr, init_value):
   nx.set_node_attributes(graph, attr, init_value)
####################################################################################



####################################################################################
# Randomizes attributes of all nodes in a graph to a value in a specified range.   #
####################################################################################
def randomize_node_attribute(graph, attr, low, high):
   for node in graph.node:
      graph.node[node][attr] = rand.randint(low, high)
####################################################################################



####################################################################################
# Randomizes node attribute boolean values given a percentage that node attributes #
# are set to true.                                                                 #
####################################################################################
def randomize_node_attribute_boolean(graph, attr, true_chance):
   for node in graph.node:
      graph.node[node][attr] = chance(true_chance)
####################################################################################



####################################################################################
# Creates an attribute with an initial value.                                      #
####################################################################################
def create_edge_attribute(graph, attr, init_value):
   nx.set_edge_attributes(graph, attr, init_value)
####################################################################################



####################################################################################
# Randomizes attributes of all nodes in a graph to a value in a specified range.   #
####################################################################################
def randomize_edge_attribute(graph, attr, low, high):
   for source in graph.edge:
      for dest in graph.edge[source]:
            if source < dest or nx.is_directed(graph):
               graph.edge[source][dest][attr] = rand.randint(low, high)
####################################################################################



####################################################################################
# Randomizes node attribute boolean values given a percentage that node attributes #
# are set to true.                                                                 #
####################################################################################
def randomize_edge_attribute_boolean(graph, attr, true_chance):
   for source in graph.edge:
      for dest in graph.edge[source]:
         if source < dest or nx.is_directed(graph):
            graph.edge[source][dest][attr] = chance(true_chance)
####################################################################################

####################################################################################
# Subgraph completion check, takes only a graph argument.                          #
####################################################################################
# Subgraph stuff
def check_subgraph_spread(graph):
   if (subgraph_max_spread(graph)):
      return 1
   else:
      if (num_flagged(graph) > 0):
         return 0 # We've finished the graph, as best we could.
      else:
         return -1 # We have 0 infected nodes. Graph failed.
####################################################################################


####################################################################################
# Determines whether or not a graph is finished by considering subgraph spread.    #
# May run into problems if directed graphs are ever considered.                    #
####################################################################################
def subgraph_max_spread(g):
   graphs = list(nx.connected_component_subgraphs(g, copy=True))
   num_subgraphs = len(graphs)
   graphs_max_spread = 0
   graphs_partial_spread = 0
   for graph in graphs:
      all_flagged = True
      has_any_flag = False
      for node in graph.node:
         if not graph.node[node]['flagged']:
            all_flagged = False
         else:
            has_any_flag = True
      if (all_flagged):
         graphs_max_spread += 1
      elif (has_any_flag == True):
         graphs_partial_spread += 1

   if graphs_max_spread >= 1 and graphs_partial_spread == 0:
      return True
   else:
      return False
####################################################################################


####################################################################################
# Returns an integer value with the number of flagged nodes                        #
####################################################################################
def num_flagged(graph):
   num_flagged = 0
   nodes = nx.get_node_attributes(graph, 'flagged')
   for val in nodes:
      if (nodes[val]):
         num_flagged += 1
   return num_flagged
####################################################################################



####################################################################################
# Rolls a chance that nodes will communicate given the weight of an edge and       #
# a given maximum weight (chance = given/maximum)                                  #
####################################################################################

def roll_weight(curr_weight, max_weight):
   # Returns the likelihood of engagement based on weight of graph nodes
   return rand.randint(1, max_weight) > (max_weight - curr_weight)

####################################################################################



####################################################################################
# Returns whether or not a round has exceeded a round limit.                       #
'''
    Args:
        curr_round: The current round of a simulation
        max_rounds: The maximum rounds a simulation should have

    Returns:
        True if a simulation has exceeded the maximum number of rounds
        False if a simulation has not exceeded the maximum number of rounds
'''
####################################################################################
def exceeded_round_limit(curr_round, max_rounds):
   return curr_round > max_rounds
####################################################################################
