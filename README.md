CONNECT-WHILE-IN-RANGE: DYNAMIC NETWORKS FROM LOCATION, RANDOM MOVEMENT, AND RANGED COMMUNICATION

This agent-based model simulates the influence of spatial constraints on network formation, and on several transmission processes simulated on that network. 
N agents with communication range r randomly move through a coordinate grid gxg, dynamically add and remove links based on communication range, 
and with some global probability P diffuse information along these links.

SCRIPTS

The folder contains 3 python files: the important ones are one for the agent update rules that the simulation consists of ("1.model"), and one ("2.plots") for creating plots and summary statistics from simulation results. Then there's a third file which creates an animated gif of one simulation run of T timesteps at desired settings, which is useful for intution. 

HOW TO RUN

1. Install packages
This code was written in Google Colab and links to the Colab files are given with each of the python files. In Colab, the packages used in this code come pre-installed and the "import [packagename] as [abbreviation]" commands included in the code files suffice. In locally run environments, enter in the terminal "pip install [packagename]". For example, for the networkx package, enter:
   ```pip install networkx```
The names of the packages used are networkx, numpy, math, scipy, copy, matpotlib, and pandas.

2. 

3. File 1: "Model": define functions and run simulation.

4. File 2: "
   


The code in "model" defines the functions that update the agents, run the simulations, and collect the output data. The files were written in Google Colab and downloaded as .py files.
Packages used are networkx, numpy, random, math, and copy. (in Colab, "import *packagename* " suffices to use these; in local environments, one can use "pip install *packagename*" to install). 
To run simulations, run the "model" code defining the functions and call the run_simulation() function, specifying the input parameters as detailed in "model." The result is a collection 
of results dictionaries that will be summarized and plotted in "plots." The packages used in that file are numpy and matplotlib. To create the results plots, run the "plots" code and call the 
summary_and_plot(), specifying the function arguments corresponding to the input parameter choices made in the run_simulation() call, as detailed in "model." Finally, "model gif" uses PIL (in Colab:
"from PIL import Image" and IPython ("from Ipython.display import display, Image), and the range model update rule also found in "model", to create an animated gif of one model run of 100 timesteps.
It's a good way of getting some intution for how the model behaves. See the "model gif" file for detailed instructions.

A model run looks like this: 

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/58f68008-731e-461e-80d7-394cbb75dc0a)

(This gif is created by the code found in file 3). 

Model results look like this: 

Network structure plots:

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/79c1d933-5417-48cd-9dad-2524cf6e2327)

Diffusion process plots:

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/b03135dc-f129-4d94-a158-31bfae792ea0)

Potion task performance plots:

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/3aa87b21-db99-4d5e-a0d0-a90c31c1c010)

Overall, the simulations show the extensive role simple physical constraints (location, communication range, and movement) can play in the formation of networks. Also simulated are some common hypothetical diffusion processes on top of these networks, in order to illustrate the differences this may lead to in outcomes of collective processes such as cultural evolution and information sharing. The most striking difference between the ranged model and the non-spatial model is in clustering: at lower to intermediate range, networks are much more clustered than in a comparable non-spatial model. This is reflected in the slower SI diffusion and faster complex contagion along networks at those settings. 






