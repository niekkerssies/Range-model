CONNECT-WHILE-IN-RANGE: DYNAMIC NETWORKS FROM LOCATION, RANDOM MOVEMENT, AND RANGED COMMUNICATION

This agent-based model simulates the influence of spatial constraints on network formation, and on several transmission processes simulated on that network. 
N agents with communication range r randomly move through a coordinate grid gxg, dynamically add and remove links based on communication range, 
and with some global probability P diffuse information along these links.

SCRIPTS

The folder contains 3 python files: the important ones are one for the agent update rules that the simulation consists of ("1.model"), and one ("2.plots") for creating plots and summary statistics from simulation results. Then there's a third file which creates an animated gif of one simulation run of T timesteps at desired settings, which is useful for intuition. 

HOW TO RUN

1. Install packages

This code was written in Google Colab and links to the Colab files are given with each of the python files. In Colab, the packages used in this code come pre-installed and the "import [packagename] as [abbreviation]" commands included in the code files suffice. In locally run environments, enter in the terminal "pip install [packagename]". For example, for the networkx package, enter:
   ```pip install networkx```.
The names of the packages used are networkx, numpy, scipy, matpotlib, and pandas.

2. File 1: Model: define functions and run simulation.

The first .py file in this repository "1. Model" contains the code required to define and run the simulations. Before running the code, the user only needs to set the argument values in the last line: the "run_simulation()" function call. This consists of setting the required arguments, and the optional arguments. The required arguments of run_simulation are: (R,r,N,g,T,Q). Choose an input parameter (r,N,g) to be varied. Input the corresponding value for Q: varying_parameter = list(range([r,N,g][Q])). So if Q = 0, r is varying; if Q = 1, N is varying. Then, for the varying parameter, put the maximum value. The simulation will run for each integer value of the parameter up to that maximum. (Note: because Python indexes start at 0, set the maximum to 1 higher than the desired included maximum). For all other values, put a constant value.

The diffusion processes are set by optional arguments in the run_simulation() function that are set to a default value if unspecified. Hence, the complete arguments taken by run_simulation() are (R, r, N, g, T, Q, P=0, N_init=0, compl=False, weight=0, CE=False, pa=0, pb=0, potion=False, pdiff=0). By default, the model simulates an SI diffusion process with infection probability P and N_init initially infected agents(see "1.Model" for explanation). To run a different diffusion process, set the corresponding boolean argument to True (compl for complex contagion, CE for cultural evolution, and potion for potion task; again see the file text for explanation) and set the relevant parameters; "weight" for complex contagion, pa and pb for cultural evolution, and pdiff for diffusion in the potion task. All of these variables specify a probability and therefore take a value between 0 and 1.

For example, for a simulation (of 100 rounds of 100 timesteps) of network structures under varying range, with complex contagion: 
```data = run_simulation(100,11,10,10,100,0,compl=True,weight=0.1``` Here, 10 agents move in a 10x10 grid, and between simulations communication range varies [0,1,2....,9,10]. 

3. File 2: Plots: define plotting and summary functions and create output visualizations.

The output of a model run done by the code in file 1 will be the "data" object, in which the network structure and diffusion process outcomes are stored. The code in the second file takes this and turns it into visualizations and summary statistics.

To plot the results, set the argument inputs in the last line (the summary_and_plot function call) and run the code (note: this assumes the code of file 1 has been executed, creating the "data" object). The arguments are results, parameter_label, CE=False, and potion=False. For "results", simply put the 'data' object defined by the run_simulation call (the result of script 1). " For "parameter_label", put the name of the varying input parameter chosen in the simulation run: "Range","N", or "g". If cultural evolution was simulated, set "CE" to True; if potion task was simulated, set "potion" to True. The result is 7 network structure plots two diffusion process plots, and dataframes containing the summary statistics visualized in these plots (see below figure). Example function call for SI diffusion and range as varying input parameter: ```summary_and_plot(data,"Range")```.

Finally, "model gif" uses PIL (in Colab: "from PIL import Image") and IPython ("from Ipython.display import display, Image), and the range model update rule also found in "model", to create an animated gif of one model run of 100 timesteps. It's a good way of getting some intuition for how the model behaves. See the "model gif" file for detailed instructions.

A model run looks like this: 

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/58f68008-731e-461e-80d7-394cbb75dc0a)

(This gif is created by the code found in file 3). 

Model results look like this: 

Network structure plots:

![Varying range N 20](https://github.com/user-attachments/assets/1c007b23-5cb9-405e-b22d-4b60775687dd)

Diffusion process plots:

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/b03135dc-f129-4d94-a158-31bfae792ea0)

Potion task performance plots:

![Untitled](https://github.com/niekkerssies/Range-model/assets/125357452/3aa87b21-db99-4d5e-a0d0-a90c31c1c010)

Overall, the simulations show the extensive role simple physical constraints (location, communication range, and movement) can play in the formation of networks. In order to illustrate the differences this may lead to in outcomes of collective processes such as cultural evolution and information sharing,  some common models of diffusion processes are also simulated. The most striking difference between the ranged model and the non-spatial model is in clustering: at lower to intermediate range, networks are much more clustered than in a comparable non-spatial model. This is reflected in the slower SI diffusion and faster complex contagion along networks at those settings. 






