# -*- coding: utf-8 -*-
"""3: Model gif

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gogCJimo-kE3XODASKNE7gC2h26T0ZUJ

This script contains the update rules as found in script 1, plus a command that saves timesteps as frames to a file that is displayed as an animated gif. This visualizes a single run of the model.
"""

import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import math
import scipy
import seaborn
import pandas
import copy

plt.rcParams.update({'figure.figsize': (10, 10)})
#this just globally sets the figure size

combination_list = [
    ['a1','a3','b2'],
    ['A1','b1','b2'],
    ['A2','a1','b1'],
    ['A3','B3','B1'],
    ['a1','b1','b3'],
    ['B1','a2','a3'],
    ['B2','a2','b1'],
    ['B3','A3','B2']
]

sorted_combination_list = []

for entry in combination_list:
  sorted_combination_list.append(sorted(entry))

discovery_list = [
    ['A1','a',48,48],
    ['A2','a',109,109],
    ['A3','a',188,188],
    ['A4','a',358,358],
    ['B1','b',48,48],
    ['B2','b',109,109],
    ['B3','b',188,188],
    ['B4','b',358,358]
]


starting_inventory = [
    ["a1", 'a', 6, 0], #Potion, trajectory, value, score
    ["a2", 'a', 8, 0],
    ["a3", 'a', 10, 0],
    ["b1", 'b', 6, 0],
    ["b2", 'b', 8, 0],
    ["b3", 'b', 10, 0]]

def combine_items(combination,i,j,G):
  discovery = []
  discovered = False
  #check if valid combination
  item_ids = sorted([i[0] for i in combination])
  #sort both so order of items doesn't matter
  for entry in combination_list:
    if item_ids == sorted(entry):
      index = sorted_combination_list.index(item_ids)
      discovery = discovery_list[index]
      if discovery not in G.nodes[i]["inventory"] and discovery not in G.nodes[j]["inventory"]:
        discovered = True
      else:
        discovered = False
  return discovery, discovered

def diffuse(agent,discovery,pdiff,G):
  neighborlist = list(G.neighbors(agent))
  for neighbor in neighborlist:
    #check if discovered item in neighbor inventory
    if discovery not in G.nodes[neighbor]["inventory"]:
      #that neighbor adds the item with probability p: innovation diffusion probability.
      if random.random() > pdiff:
        G.nodes[neighbor]["inventory"].append(discovery)

def potion_task(G,pdiff,orderlist):
  #If you like you can define the lists and parameters given globally in "initialization"
  #here instead.
  for i in orderlist:
    #select partner:
    neighbors_list = list(G.neighbors(i))
    #If there are neighbors (list is non-empty), do the interaction:
    if neighbors_list:
      j = random.choice(neighbors_list)
      combination = select_item(i,j,G)
      discovery, discovered = combine_items(combination,i,j,G)
      if discovered:
        #Update inventories to include the discovered item (again as [Id,Trajectory,Value,Score])
        G.nodes[i]["inventory"].append(discovery)
        G.nodes[j]["inventory"].append(discovery)
        if pdiff > 0:
          diffuse(i,discovery,pdiff,G)
          diffuse(j,discovery,pdiff,G)
    scores = [item[3] for item in G.nodes[i]["inventory"]]
    #set score to highest valued current item
    G.nodes[i]["score"] = max(scores)
  return G

def initialize_graph(N,g,N_init,Q,i):
  coordinatespace = [(x,y) for x in range(g) for y in range(g)]

  G = nx.Graph()

  #Again, if varying parameter is N, create i agents rather than N.
  if Q == 1:
    #choose N unique positions as starting positions:
    initpos = random.sample(coordinatespace,i)
    for j in range(i):
      G.add_node(j, position = initpos[j])
      if j < N_init:
        G.nodes[j]["trait"]=1
      else:
        G.nodes[j]["trait"]=0

  #if varying parameter is not N, initialize a graph of size N.
  else:
    initpos = random.sample(coordinatespace,N)
    for n in range(N):
      G.add_node(n, position=initpos[n])
      if n < N_init:
        G.nodes[n]["trait"]=1
      else:
        G.nodes[n]["trait"]=0

  return G

def connect_while_in_range(G, g, Range, P, compl = False, weight=0, potion = False, pdiff = 0):
  orderlist = random.sample(G.nodes,len(G.nodes))
  #random update order each timestep: take a random sample without replacement of the set of nodes of G,
  #of size N. In other words, arrange the nodes in a random order, which will be used to iterate over this timestep.

  #Movement:
  for i in orderlist:
    #list of positions currently occupied by other agents:
    occupied = list(G.nodes[j]["position"] for j in G.nodes)
    #retreive own current position:
    x, y = G.nodes[i]["position"]
    #Create list of positions in the Moore neighborhood:
    #(there's a smarter way of doing this with list comprehension, but that statement is about as long as just putting in the coordinates)
    neighborhood = [(x-1,y+1),(x,y+1),(x+1,y+1),(x-1,y),(x,y),(x+1,y),(x-1,y-1),(x,y-1),(x+1,y-1)]
    #Grid boundaries: if any of the available neighborhood positions would be below 0 or above g, delete them from the options:
    filtered_neighborhood = [(nx, ny) for nx, ny in neighborhood if 0 <= nx < g and 0 <= ny < g]
    #only move if position available (so if the list 'available' is non-empty), otherwise stay at current position:
    available = [pos for pos in filtered_neighborhood if pos not in occupied]
    if available:
      G.nodes[i]['position'] = random.choice(available)

  #Potion task:
  if potion:
    G = potion_task(G,pdiff,orderlist)

  else:

    #Complex contagion: transmission probability is a weighted sum of the number of neighbors with trait = 1.
    if compl:
      for i in orderlist:
        count = 0
        for j in G.neighbors(i):
            if G.nodes[j]['trait'] == 1:
                count += 1

        if G.nodes[i]['trait'] == 0:
            # Complex contagion: Probability of adoption depends on the count of adopting neighbors
            adoption_prob = P + ((count/len(G.nodes)) * weight)
            if random.random() < adoption_prob:
                G.nodes[i]['trait'] = 1
    else:

      #SI diffusion:
      for i in orderlist:
        for j in G.neighbors(i):
          if G.nodes[i]["trait"] == 1 and G.nodes[j]['trait'] == 0:
            if random.random() < P:
              G.nodes[j]["trait"] = 1
            if G.nodes[j]["trait"] == 1 and G.nodes[i]['trait'] == 0:
              if random.random() < P:
                G.nodes[i]["trait"] = 1

  #Link updating:
  for i in orderlist:
    for j in orderlist:
      if j > i:
        #if within range, create link; if an existing edge is now out of range, remove it.
        ij_distance = math.sqrt((G.nodes[j]["position"][0] - G.nodes[i]["position"][0]) ** 2 +
                                      (G.nodes[j]["position"][1] - G.nodes[i]["position"][1]) ** 2)
        if ij_distance <= Range:
          G.add_edge(i, j)
        elif G.has_edge(i, j):
          G.remove_edge(i, j)

  return G

def connect_at_random(G_null,pc,P,compl=False,weight=0,potion=False,pdiff=0):
  pdis = 1-pc
  orderlist = random.sample(G_null.nodes,len(G_null.nodes))

  if potion:
    G_null = potion_task(G_null,pdis,orderlist)

  else:

    #Complex contagion: transmission probability is a weighted sum of the number of neighbors with trait = 1.
    if compl:
      for i in orderlist:
        count = 0
        for j in G_null.neighbors(i):
            if G_null.nodes[j]['trait'] == 1:
                count += 1

        if G_null.nodes[i]['trait'] == 0:
            # Complex contagion: Probability of adoption depends on the count of adopting neighbors
            adoption_prob = P + ((count/len(G_null.nodes)) * weight)
            if random.random() < adoption_prob:
                G_null.nodes[i]['trait'] = 1
    else:

      #Diffusion
      for i in orderlist:
        for j in G_null.neighbors(i):
          if G_null.nodes[i]["trait"] == 1 and G_null.nodes[j]['trait'] == 0:
            if random.random() < P:
              G_null.nodes[j]["trait"] = 1
          if G_null.nodes[j]["trait"] == 1 and G_null.nodes[i]['trait'] == 0:
            if random.random() < P:
              G_null.nodes[i]["trait"] = 1

  #Link updating
  for i in orderlist:
    for j in orderlist:
      if j > i:
        if (not G_null.has_edge(i,j)) and (random.random() < pc):
          #connect if random value between 0 and 1 is lower than the connection chance.
          #At 1 it is always lower, at 0 it never is.
          G_null.add_edge(i, j)
        if G_null.has_edge(i, j) and random.random() < pdis:
          G_null.remove_edge(i, j)

  return G_null

from PIL import Image

g=50
N=50
r=8
T=100

G = initialize_graph(N,g,1,0,r)

positions = nx.get_node_attributes(G,"position")
nodecolor = ["tab:red" if G.nodes[i]["trait"] == 1 else "tab:blue" for i in G.nodes]

nx.draw_networkx(G,node_size=40,labels=positions,pos=positions)

frames = []

for t in range(T):
  positions = nx.get_node_attributes(G,"position")
  nodecolor = ["tab:red" if G.nodes[i]["trait"] == 1 else "tab:blue" for i in G.nodes]
  nx.draw_networkx(G,node_size=40,labels=positions,pos=positions,node_color=nodecolor)   #labels=nx.get_node_attributes(G,"position"))
  plt.title(f'Range={r}, N={N}, grid={g}x{g}, T={t + 1}')
  # Save the current frame as an image
  filename = f'frame_{t + 1:03d}.png'
  plt.savefig(filename, dpi=100, bbox_inches='tight')
  plt.close()  # Close the current plot to release memory
  # Append the saved frame to the list
  frames.append(Image.open(filename))
  #update the network timestep
  G = connect_while_in_range(G,g,r,0.05)

# Create a GIF from the saved frames
frames[0].save('animation.gif', save_all=True, append_images=frames[1:], duration=300, loop=0)

from IPython.display import display, Image

display(Image(filename='animation.gif'))