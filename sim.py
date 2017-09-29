#!/usr/bin/env python

#######################
# PROJECT RUMOR MILL
# ==================
# Project Director:
# Michael Bigrigg
# 
# Team Members:
# Emily Hannah
# Tianjian Meng
# Julian Monticelli
#######################

###############
# Important!! #
# Whitespace! #
# -> 3 spaces #
###############


import argparse         # Parse command line args
import copy             # For copying graphs
import networkx as nx   # GraphML
import random as rand

# Transmission variables
talkToTransmit = True   # Transmission = just talking?
chance_to_spread = 0.01 # If transmit =/= talk, what is the chance upon talking

# Forgetting variables
can_node_forget = True
node_forget_chance = 0.01 # Chance for node to forget

maximum_allowed_simulation_rounds = 1000 # 1 million runs currently
num_runs = 10       # Default number of runs


####################################################################################
# Program entry point. Setup, etc.                                                 #
####################################################################################
def main():
   # TODO: Program args
   
   # Read in a graph
   simulation_graph = nx.read_graphml('simplemodel.graphml')
   
   # Initialize the graph with attributes we need
   init(simulation_graph, 'n10')
   
   # Run a simulation 100 times
   simulate(simulation_graph, num_runs)

####################################################################################





####################################################################################
# Simulation function - to be changed and altered. Highly volatile.                #
####################################################################################
def simulate(graph, num_simulations):
   weight_max = max_weight(graph)
   sum_time = 0
   num_fails = 0
   current_run = 1
   total_flagged = 0
   while (current_run <= num_simulations):
      graph_instance = copy.deepcopy(graph)
      run_time,num_flagged = run(graph_instance, weight_max)
      total_flagged += num_flagged
      if (run_time < 0):
         print 'Run ' + str(current_run) + ' failed! ' + str(num_flagged) + '/' + str(len(graph.node)) + ' flagged. (' + str(successPercent(graph, num_flagged)) + '% complete)'
         num_fails += 1
      else:
         print 'Run ' + str(current_run) + ' took ' + str(run_time) + ' rounds. ' + str(len(graph.node)) + '/' + str(len(graph.node)) + ' flagged. (100% complete)'
         sum_time += run_time

      current_run += 1
   if (num_simulations == num_fails): # Avoid division by 0
      print 'All runs failed. maximum_allowed_simulation_rounds = ' + str(maximum_allowed_simulation_rounds) + ' (Average completion rate: ' + str(totalSuccessPercent(graph, total_flagged, num_simulations)) + '%)'
   else:
      print str(num_simulations) + ' simulations finished. ' + str(num_fails) + ' simulations failed. Average run time: ' + str(sum_time/ (num_simulations - num_fails) ) + ' rounds'
      print 'Average completion rate: ' + str(totalSuccessPercent(graph, total_flagged, num_simulations)) + '%)'
####################################################################################




####################################################################################
# Gets a percentage of success based on a graph node count and the number of       #
# nodes that were flagged.                                                         #
####################################################################################
def successPercent(graph, num_flagged):
   return 100 * num_flagged / float(len(graph.node))
####################################################################################



####################################################################################
# Returns the total percentage of success given a graph, the number of flagged     #
# nodes and the total number of simulations.                                       #
####################################################################################
def totalSuccessPercent(graph, num_flagged, num_simulations):
   return 100 * num_flagged / float((len(graph.node) * num_simulations))
####################################################################################


####################################################################################
# Initialize the graph with attributes that are necessary to run a simulation.     #
# Takes a graph and a String node (i.e., 'n10') to initialize as flagged.          #
# Also initializes uninitialized weights on graphs as 1.                           #
####################################################################################
def init(graph, node):
   # Give all nodes a false flag
   nx.set_node_attributes(graph, 'flagged', False)
   
   # Get graph-given weight attributes and save them
   dict = nx.get_edge_attributes(graph, 'weight')
   
   # Write 1 weight to all edges
   nx.set_edge_attributes(graph, 'weight', 1)
   
   for n1,n2 in dict:
      graph.edge[n1][n2]['weight'] = dict[n1,n2]
   
   #print dict
   
   #for e in nx.get_edge_attributes(graph, 'weight'):
      #print e
   
   # Set an arbitrary node
   graph.node[node]['flagged'] = True
####################################################################################





####################################################################################
# Pass in a graph, get the integer maximum weight of all edges                     #
####################################################################################
def max_weight(graph):
   max_weight = 0
   dict = nx.get_edge_attributes(graph, 'weight')
   for val in dict:
      max_weight = max(max_weight, dict[val])
   #print max_weight
   return max_weight
####################################################################################




####################################################################################
# A single run of a simulation                                                     #
####################################################################################
def run(graph, max_weight):
   # Declare data to gather
   round_num = 0
   num_flags = num_flagged(graph)
   # print 'Total nodes: ' + str(len(graph.node))
   # TODO: Variable finished condition for easy hook mod
   # Run loop
   
   while(finished(graph, round_num) == 0):
      round_num += 1

      # Run the round and return the number of successes and add it to the total_successes
      #print round_num #
      num_flags += round(graph, round_num, max_weight)

   # Check why we quit the simulation
   if (finished(graph, round_num) > 0): # If we've finished the graph
      return round_num,num_flags
   else:
      return -1,num_flags # Fail code
####################################################################################




####################################################################################
# A step in the simulation                                                         #
####################################################################################
def round(graph, round_num, max_weight):
   graphcopy = copy.deepcopy(graph)
   given_flags = 0
   forgot_flags = 0
   for n in nx.nodes(graph):
      # For directed graphs, consider flagged only
      if (graph.node[n]['flagged']):
         
         # Node forgetting
         if (can_node_forget):
            if (chance(node_forget_chance)):
                # Wipe flag from both graph and graphcopy
                graph.node[n]['flagged'] = False
                graphcopy.node[n]['flagged'] = False
                forgot_flags += 1
                break # Skip this node because it no longer has a flag

         # Check the unedited copy graph for flagged neighbors
         for g in graphcopy.edge[n]:
            # If the graph node in both the copy and original aren't flagged
            if (not graphcopy.node[g]['flagged'] and not graph.node[g]['flagged']):
               #print '!!! ' + g + ' is flagged'    #  Debug
               #print 'graph.edge[' + str(n) + ']: ' + str(graph.edge[n])
               
               # To output graph edge weights - I have no tests yet
               #print 'Graph edge weight: ' + str(graph.edge[n][g]['weight'])
               
               if (will_spread(n, g, graph, max_weight)):
                  graph.node[g]['flagged'] = True
                  # Increment the number of given_flags this round
                  given_flags += 1
                  #print '[' + g + ']: ' + str(graph.node[g]['flagged']
   return given_flags-forgot_flags # TODO: return forgot flags and given flags
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
################################################################



####################################################################################
# Determine if a given source node will transmit information to a given node       #
####################################################################################
def will_spread(source, dest, graph, max_weight):
   # TODO: Add more dynamic way to spread flags from nodes to nodes
   
   # Get current weight
   curr_weight = graph.edge[source][dest]['weight']
   
   # Will they engage at all? This consults the weight of their edge
   if ( roll_weight (curr_weight , max_weight ) ):
      if (talkToTransmit):
          return True
      else:
         # This is the chance that their engagement will exchange information
         if (chance(chance_to_spread)):
            return True
   return False
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
# Rolls a chance that nodes will communicate given the weight of an edge and       #
# a given maximum weight (chance = given/maximum)                                  #
####################################################################################

def roll_weight(curr_weight, max_weight):
   # Returns the likelihood of engagement based on weight of graph nodes
   return rand.randint(0, max_weight) > max_weight - curr_weight


####################################################################################




####################################################################################
# Determines whether or not a graph is finished                                    #
####################################################################################
def finished(graph, current_round):
   # Get all attributes and store them in a dictionary
   dict = nx.get_node_attributes(graph, 'flagged')
   
   # Make sure we haven't hit the maximum allowed round
   if (current_round > maximum_allowed_simulation_rounds):
      return -1 # -1 means we ran out of allowed rounds
   
   # Iterate the nodes and see if they're flagged or not 
   for val in dict:
      if(not dict[val]):
         #print '[' + val  + ']: ' + str(dict[val])
         return 0 # 0 is an incomplete graph
   return 1 # 1 is a successful graph


####################################################################################


###########################
# END OF FUNCTIONS.       #
###########################
if __name__ == "__main__":
   main()
#######i####################
