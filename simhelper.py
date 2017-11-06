import networkx as nx
import random as rand
import datetime
from time import sleep

import simdefaults as defaults



####################################################################################
# Returns an integer value with the number of flagged nodes given an attribute     #
####################################################################################
def num_flagged(graph, attr):
   num_flagged = 0
   nodes = nx.get_node_attributes(graph, attr)
   for val in nodes:
      if (nodes[val]):
         num_flagged += 1
   return num_flagged
####################################################################################



####################################################################################
'''
Converts a numerator and a denominator into a percentage.
'''
####################################################################################
def percent(numerator, denominator):
   return 100 * numerator / float(denominator)
####################################################################################



####################################################################################
'''
Gets a percentage of flagged nodes on the graph handed into it.
nodes that were flagged.
    Args:
        graph: A graph for our simulation
        num_flagged: The number of flagged nodes

    Returns:
        A percentage of nodes which are flagged (0% - 100%)

'''
####################################################################################
def percent_flagged(graph, num_flagged):
   return 100 * num_flagged / float(len(graph.node))
####################################################################################



####################################################################################
'''
Returns the total percentage of success given a graph, the number of flagged nodes 
and the total number of simulations.
    Args:
        graph: A graph for our simulation
        num_flagged: The number of flagged nodes
        num_simulations: The number of simulations that happened with the input graph

    Returns:
        A percent of flagged nodes across num_simulations simulations (0% - 100%)
'''
####################################################################################
def total_percent_flagged(graph, num_flagged, num_simulations):
   return 100 * num_flagged / float((len(graph.node) * num_simulations))
####################################################################################



####################################################################################
'''
Pass in a graph, get the integer maximum weight of all edges
    Args:
        graph: A graph for our simulation

    Returns:
        A maximum weight across all edges
'''
####################################################################################
def max_weight(graph):
   max_weight = float('-inf')
   dict = nx.get_edge_attributes(graph, 'weight')
   for val in dict:
      max_weight = max(max_weight, dict[val])
   return max_weight
####################################################################################



####################################################################################
'''
Given a percentage chance (0.0 - 1.0), roll for that chance.
    Args:
        percentage_chance: The percentage chance for a successful row

    Returns:
        True if the RNG roll is less than or equal to the percentage_chance
        False if the RNG roll is greater than the percentage_chance
'''
####################################################################################
def chance(percentage_chance):
   if (percentage_chance > 1):
      print 'Percentage chance should never be MORE than 1. Even if you want 100% rolls. (PC: ' + str(percentage_chance) + ')'
      return True
   if (percentage_chance <= 0):
      print 'Percentage chance being less than or equal to 0 will always result in a failure. (PC: ' + str(percentage_chance) + ')' 
      return False
   if (rand.random() <= percentage_chance):
      return True
####################################################################################



####################################################################################
'''
Dumps information about the given graph.
    Args:
        graph: A graph for our simulation
'''
####################################################################################
def output_graph_information(graph):
   print '*' * defaults.asterisk_space_count
   print 'Graph has ' + str(graph.number_of_nodes()) + ' node(s) and ' + str(graph.number_of_edges()) + ' edge(s).'
   print 'Density: ' + str(nx.density(graph))
   print 'Max weight of edges: ' + str(max_weight(graph))
   if nx.is_connected(graph):
      print 'Graph is completely connected.'
   else:
      print 'Graph is disjoint.'
   #print 'Betweenness centrality: ' + str(nx.betweenness_centrality(graph)) # It can be done!
   print '*' * defaults.asterisk_space_count
####################################################################################



####################################################################################
'''
Returns the total number of nodes in a graph. 
    Args:
        graph: A graph for our simulation

    Returns:
        The number of nodes in a graph
'''
####################################################################################
def num_nodes(graph):
   return nx.number_of_nodes(graph)
####################################################################################



####################################################################################
'''
Returns a string with the date and the time.
'''
####################################################################################
def date_time():
   return datetime.datetime.now()
####################################################################################



####################################################################################
'''
Returns a string with the date and the time.
'''
####################################################################################
def time():
   now = datetime.datetime.now()
   return datetime.time(now.hour, now.minute, now.second)
####################################################################################



####################################################################################
'''
Sleeps for a number of milliseconds
'''
####################################################################################
def sleep_ms(ms):
   sleep(((float)(ms)) / ((float)(1000)))
####################################################################################



####################################################################################
'''
Returns the difference between two timestamps.
    Args:
        ts1: Timestamp 1
        ts2: Timestamp 2

    Returns:
        Difference in time in seconds
'''
####################################################################################
def time_diff(ts1, ts2):
   if ts1 > ts2:
      td = ts1 - ts2
   else:
      td = ts2 - ts1
   td = int(td.total_seconds())
   return td
####################################################################################



####################################################################################
'''
Creates an attribute with an initial value.
    Args:
        graph: A graph for our simulation
        attr: An attribute name
        init_value: A value that we will initialize our attribute with
'''
####################################################################################
def create_node_attribute(graph, attr, init_value):
   nx.set_node_attributes(graph, attr, init_value)
####################################################################################



####################################################################################
'''
Creates an attribute with an initial value on a specific node.
    Args:
        graph: A graph for our simulation
        node: A specific node for 
        attr: An attribute name
        init_value: A value that we will initialize our attribute with
'''
####################################################################################
def create_single_node_attribute(graph, node, attr, init_value):
   graph.node[node][attr] = init_value
####################################################################################



####################################################################################
'''
Creates an attribute with an initial value given a list of nodes.
    Args:
        graph: A graph for our simulation
        node_list: A list of nodes for which to modify an attribute
        attr: An attribute name
        init_value: A value that we will initialize our attribute with
'''
####################################################################################
def create_node_list_attribute(graph, node_list, attr, init_value):
   for node in node_list:
      graph.node[node][attr] = init_value
####################################################################################



####################################################################################
'''
Randomizes attributes of all nodes in a graph to a value in a specified range.
    Args:
        graph: A graph for our simulation
        attr: An attribute name
        low: A low value (inclusive) for our range
        high: A high value (inclusive) for our range
'''
####################################################################################
def randomize_node_attribute(graph, attr, low, high):
   for node in graph.node:
      graph.node[node][attr] = rand.randint(low, high)
####################################################################################



####################################################################################
'''
Randomizes attributes of a single node in a graph to a value in a specified range.
    Args:
        graph: A graph for our simulation
        node: A specific node in the graph
        attr: An attribute name
        low: A low value (inclusive) for our range
        high: A high value (inclusive) for our range
'''
####################################################################################
def randomize_single_node_attribute(graph, node, attr, low, high):
   graph.node[node][attr] = rand.randint(low, high)
####################################################################################



####################################################################################
'''
Randomizes attributes of all nodes in a graph to a value in a specified range.
    Args:
        graph: A graph for our simulation
        node_list: A list of nodes for which to modify an attribute
        attr: An attribute name
        low: A low value (inclusive) for our range
        high: A high value (inclusive) for our range
'''
####################################################################################
def randomize_node_list_attribute(graph, attr, low, high):
   for node in node_list:
      graph.node[node][attr] = rand.randint(low, high)
####################################################################################



####################################################################################
'''
Randomizes node attribute boolean values given a percentage that node attributes 
are set to true.
    Args:
        graph: A graph for our simulation
        attr: An attribute name
        true_chance: A chance that your boolean will be initialized as true
                     given any node
'''
####################################################################################
def randomize_node_attribute_boolean(graph, attr, true_chance):
   for node in graph.node:
      graph.node[node][attr] = chance(true_chance)
####################################################################################



####################################################################################
'''
Randomizes a single node attribute boolean values given a percentage that node
attributes are set to true.
    Args:
        graph: A graph for our simulation
        node: A node whose attribute we will modify
        attr: An attribute name
        true_chance: A chance that your boolean will be initialized as true
                     given any node
'''
####################################################################################
def randomize_single_node_attribute_boolean(graph, node, attr, true_chance):
   graph.node[node][attr] = chance(true_chance)
####################################################################################



####################################################################################
'''
Randomizes list nodes attribute boolean values given a percentage that node attributes 
are set to true.
    Args:
        graph: A graph for our simulation
        node_list: A list of nodes for which to modify an attribute
        attr: An attribute name
        true_chance: A chance that your boolean will be initialized as true
                     given any node
'''
####################################################################################
def randomize_node_list_attribute_boolean(graph, node_list, attr, true_chance):
   for node in node_list:
      graph.node[node][attr] = chance(true_chance)
####################################################################################



####################################################################################
'''
Creates an edge attribute with an initial value.
    Args:
        graph: A graph for our simulation
        attr: An attribute name
        init_value: A value that the attribute will be initialized to
'''
####################################################################################
def create_edge_attribute(graph, attr, init_value):
   nx.set_edge_attributes(graph, attr, init_value)
####################################################################################



####################################################################################
'''
Creates a single edge attribute with an initial value.
    Args:
        graph: A graph for our simulation
        u: The source node of an edge
        v: The destination node of an edge
        attr: An attribute name
        init_value: A value that the attribute will be initialized to
'''
####################################################################################
def create_single_edge_attribute(graph, u, v, attr, init_value):
   graph.edge[u][v][attr] = init_value
####################################################################################



####################################################################################
'''
Creates an edge attribute with an initial value across a list of edges.
    Args:
        graph: A graph for our simulation
        edge_list: A list of edges for which to modify an attribute
        attr: An attribute name
        init_value: A value that the attribute will be initialized to
'''
####################################################################################
def create_edge_list_attribute(graph, edge_list, attr, init_value):
   for u,v in edge_list:
      graph.edge[u][v][attr] = init_value
####################################################################################



####################################################################################
'''
Randomizes attributes of all edges in a graph to a value in a specified range.
    Args:
        graph: A graph for our simulation
        attr: An attribute name
        low: A low value (inclusive) for our range
        high: A high value (inclusive) for our range
'''
####################################################################################
def randomize_edge_attribute(graph, attr, low, high):
   for source in graph.edge:
      for dest in graph.edge[source]:
            if source < dest or nx.is_directed(graph):
               graph.edge[source][dest][attr] = rand.randint(low, high)
####################################################################################



####################################################################################
'''
Randomizes attributes of a single edge in a graph to a value in a specified range.
    Args:
        graph: A graph for our simulation
        u: A source node for our edge
        v: A destination node for our edge
        attr: An attribute name
        low: A low value (inclusive) for our range
        high: A high value (inclusive) for our range
'''
####################################################################################
def randomize_single_edge_attribute(graph, u, v, attr, low, high):
   graph.edge[u][v][attr] = rand.randint(low, high)
####################################################################################



####################################################################################
'''
Randomizes attributes of all edges in a graph to a value in a specified range.
    Args:
        graph: A graph for our simulation
        edge_list: A list of edges for which to modify attributes
        attr: An attribute name
        low: A low value (inclusive) for our range
        high: A high value (inclusive) for our range
'''
####################################################################################
def randomize_edge_list_attribute(graph, edge_list, attr, low, high):
   for u,v in edge_list:
      graph.edge[u][v][attr] = rand.randint(low, high)
####################################################################################



####################################################################################
'''
Randomizes edge attribute boolean values given a percentage that edge attributes
are set to true.
    Args:
        graph: A graph for our simulation
        attr: An attribute name
        true_chance: A chance that for any edge it will initialize to true
'''
####################################################################################
def randomize_edge_attribute_boolean(graph, attr, true_chance):
   for source in graph.edge:
      for dest in graph.edge[source]:
         if source < dest or nx.is_directed(graph):
            graph.edge[source][dest][attr] = chance(true_chance)
####################################################################################



####################################################################################
'''
Randomizes a single edge boolean value given a percentage that edge attributes
are set to true.
    Args:
        graph: A graph for our simulation
        u: A source node for our edge
        v: A destination node for our edge
        attr: An attribute name
        true_chance: A chance that for any edge it will initialize to true
'''
####################################################################################
def randomize_single_edge_attribute_boolean(graph, u, v, attr, true_chance):
   graph.edge[u][v][attr] = chance(true_chance)
####################################################################################



####################################################################################
'''
Randomizes edge list attribute boolean values given a percentage that edge attributes
are set to true.
    Args:
        graph: A graph for our simulation
        attr: An attribute name
        true_chance: A chance that for any edge it will initialize to true
'''
####################################################################################
def randomize_edge_attribute_boolean(graph, edge_list, attr, true_chance):
   for u,v in edge_list:
      graph.edge[u][v][attr] = chance(true_chance)
####################################################################################



####################################################################################
'''
Subgraph completion check, takes only a graph argument.
    Args:
        graph: A graph for our simulation

    Returns:
        1 if we have finished the graph (as best we could)
        0 if we have not finished the graph (but we could still continue)
       -1 if we have 0 nodes left in all subgraphs
'''
####################################################################################
def check_subgraph_spread(graph):
   if (subgraph_max_spread(graph)):
      return 1 # We have finished the graph as best we could
   else:
      if (num_flagged(graph) > 0):
         return 0 # We have not finished the graph
      else:
         return -1 # We have 0 infected nodes. Graph failed.
####################################################################################


####################################################################################
'''
Determines whether or not a graph is finished by considering subgraph spread.
May run into problems if directed graphs are ever considered.
    Args:
        graph: A graph for our simulation

    Returns:
        True if there is at least one subgraph complete, but none partially complete
        False if there is not at least one subgraph complete, or at least one
              partially complete graph
'''
####################################################################################
def subgraph_max_spread(graph):
   graphs = list(nx.connected_component_subgraphs(graph, copy=True))
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
'''
Rolls a chance that nodes will communicate given the weight of an edge and
a given maximum weight (chance = given/maximum)
    Args:
        curr_weight: The current weight in consideration (our chance numerator)
        max_weight: The maximum weight in a graph (our chance denominator)

    Returns:
        True if our weight roll satisfies a percentage chance
        False if our weight roll does not satisfy a percentage chance
'''
####################################################################################
def roll_weight(curr_weight, max_weight):
   # Returns the likelihood of engagement based on weight of graph nodes
   return rand.randint(1, max_weight) > (max_weight - curr_weight)
####################################################################################



####################################################################################
'''
Returns whether or not a round has exceeded a round limit.
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



####################################################################################
'''
Modifies the graph and adds and removes edges and nodes that are provided.
    Args:
        graph: The current graph for the simulation
        add_node_list: A list of nodes to be added
        remove_node_list: A list of nodes to be removed
        add_edge_list: A list of edges to be added
        remove_edge_list: A list of edges to be removed
'''
####################################################################################
def modify_graph(graph, add_node_list, remove_node_list, add_edge_list, remove_edge_list):
   modify_graph_edges(graph, add_edge_list, remove_edge_list)
   modify_graph_nodes(graph, add_node_list, remove_node_list)
####################################################################################



####################################################################################
'''
Modifies the graph and specifically deals with removing edges.
    Args:
        graph: The current graph for the simulation
        add_edge_list: A list of edges to be added
        remove_edge_list: A list of edges to be removed
'''
####################################################################################
def modify_graph_edges(graph, add_edge_list, remove_edge_list):
   for v1,v2 in remove_edge_list:
      graph.remove_edge(v1, v2)
   for v1,v2 in add_edge_list:
      graph.add_edge(v1, v2)
####################################################################################



####################################################################################
'''
Modifies the graph and specifically deals with removing nodes.
    Args:
        graph: The current graph for the simulation
        add_node_list: A list of nodes to be added
        remove_node_list: A list of nodes to be removed
'''
####################################################################################
def modify_graph_nodes(graph, add_node_list, remove_node_list):
   for v in remove_node_list:
      graph.remove_node(v)
   for v in add_node_list:
      graph.add_node(v)
####################################################################################



####################################################################################
'''
Takes an edge list and appends a (node, node) tuple to represent an edge.
    Args:
        edge_list: A list that holds edges
        u: The "source" node from an edge (arbitrary if undirected)
        v: The "destination" node from an edge (arb. if undirected)
        undirected: An assumed-true variable that dictates whether we should consider
                    both edges u,v and v,u
'''
####################################################################################
def add_edge_to_list(edge_list, u, v, undirected=True):
   # If a graph is undirected, check edge v,u as well as u,v
   if (undirected):
      if (tuple([v,u]) in edge_list):
         return # We do not want to continue

   # If there is not a conflict in the list, add the list
   if (tuple([u,v]) not in edge_list):
      edge_list.append(tuple([u, v]))
####################################################################################



####################################################################################
'''
Helper template.
    Args:
        arg1: Description
'''
####################################################################################
####################################################################################



####################################################################################
'''
Takes a list and appends a node to the list.
    Args:
        node_list: A list that holds nodes
        node: A node to be added to a list
'''
####################################################################################
def add_node_to_list(node_list, node):
   if (node not in node_list):
      node_list.append(node)
####################################################################################
