This agent-based model simulates the influence of spatial constraints on network formation, and on several transmission processes along the network. 
N agents with communication range r randomly move through a coordinate grid gxg, dynamically add and remove links based on communication range, 
and with some global probability P diffuse information along these links.

The folder contains 2 python files: the important ones are one for the agent update rules, one for running the simulation, and one for creating plots and summary statistics from simulation results. Then there's a fourth file which creates an animated gif of one simulation run of T timesteps at desired settings, which is useful for intution. 

A model run looks like this: 

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/58f68008-731e-461e-80d7-394cbb75dc0a)

(This gif is created by the code found in file 3). 

Model results look like this: 

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/79c1d933-5417-48cd-9dad-2524cf6e2327)




