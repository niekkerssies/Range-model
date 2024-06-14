from model import *
import multiprocessing as mp

# Your parameters go here
R = 100
r = [i for i in range(1,11)]
N = 10
g = 10
T = 100
Q = 0
P = 0.05 
N_init = 1
compl = False
weight = 0
CE = False
pa = 0
pb = 0
potion = False
pdiff = 0

if __name__ == '__main__':
	# Example: I put your parameters and created a list comp where it runs through ranges in r.
	# Note you could nest all of this inside a loop over another parameter too!
	params = [(R,ran,N,g,T,Q,P,N_init,compl,weight,CE,pa,pb,potion,pdiff) for ran in r]
	# Maximum number of processes you can run in parallel (i.e., number of CPU cores)
	max_processes = mp.cpu_count()
	# Number of processes you want to run
	num_processes = 10
	# Checks to see if the num of processes exceeds the max on your machine
	if num_processes > max_processes:
		return print(f'Specified number of processes {num_processes} exceeds the maximum of {max_processes}')
	else:
		# Creates pool for mp. The close() and join()
		pool = mp.Pool(processes=num_processes)
		# Unpacks the arguments from each tuple and passes them to the run_simulation function
		pool.starmap(run_simulation, params)
		# Called when mp is finished
		pool.close()
		# Waits for all worker processes to terminate
		pool.join()