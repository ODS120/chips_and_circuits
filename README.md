'Chips and Circuits'
=============
### Study course assignment
### Programmeertheorie - Final assignment
### Minor Programmeren Najaar 2020-2021
### Universiteit van Amsterdam
### Team'JOM-Intelligence'
#### Martijn van Veen, Olaf Stringer, Jan-Joost Raedts


## Introduction
The setup of this assignment is creating an algorithm that is able to find an optimal routing of wires connecting several (uniform)logic-gates that form a hypothetical microchip.
Given are a list of three chips with the location of its gates and three lists of different configurations of required connections between these gatges ('netlists') on each of those chips. All lists are in .csv format. These chip-netlists combinations vary in size and (potential) complexity.
The metric used to judge an algorithm’s efficiency (and to compare them) is the total ‘cost’ of an algorithm.

Cost is calculated through a formula that adds up the number of wires laid to connect all gates by an algorithm, added to an additional cost of ‘300’ for each crossing wire (which in the microchip-analogy, need to be avoided because of short circuiting and heat risks)

The gates are located on a one-level x,y Mahattan-style grid'ed field, but the algorithms are allowed to take up to seven layers of x,y,z routing space on top of that (each step up or down being one additional ‘cost’).

Throughout the 4-week course, along several ‘Milestones’ two final algorithms were to be created in any (of the in previous parts of the Minor introduced) programming language of choice. The basis for the choices to be made was formed by an introduction to heuristics and programmingtheory during this course.

The program created for this assignment has to be able to hold a data structure for a grid and fixed gates, for a netlist and have a way of calculating and presenting the chosen paths and total cost.
A more optimal route is a lower cost route.
These are the final two algoritms created by this team:


## First algorithm
The first algorithm one can choose from is a `Best First Search` algorithm. To properly run this, the following command line has to be used and altered:
`python main.py print.csv netlist.csv`
Be sure to use the correct python call. The `print.csv` file has to be altered regarding the chip one wishes to use (print_0/print_1/print_2), while the `netlist.csv` file is altered to one of the netlists (netlist_1, netlist_2, etc).
The algorithm itself then takes these inputs and processes them. The order of connections indicated in the netlist will be the first order that is used. After it is able to connect all the gates, or after it has made 10 attempt to do so but failed ten times, a new order will be initiated. This will be done four times and can be sumarised as follows:
- netlist order
- reversed netlist order
- smallest distance between gates to largest distance
- largest distance between gates to smallest distance
Each aformentioned attempt within one order will make a slight change. The gates which could not be connected by the algorithm will be removed from its original place in the list and moved to the front. This way it is certain that the they are able to connect after which it will attempt to connect the remainder of gates.
To further delve into the algorithm, after it has succeeded in connected two gates, it will not automatically use that path. It will retrace its steps to see if another, cheaper path is possible. Only when all the other options have been looked into, will it save the cheapest path.
If a connection order has been able to connect all gates, these results will be saved as a csv file. In the case that a later order manages to connect the gates with cheaper results, the existing csv will be overwritten and the cheapest will be saved.


## Second algorithm
The second algorithm is a `Hill climber` based algorithm. To properly run this, the following command line has to be used and altered:
`python main.py print.csv netlist.csv`
Be sure to use the correct python call. The `print.csv` file has to be altered regarding the chip one wishes to use (print_0/print_1/print_2), while the `netlist.csv` file is altered to one of the netlists (netlist_1, netlist_2, etc).

The algorithm will use the order of connections in the netlist file to connect the gates based on a 'best step' approach. Starting at the source node, the algorithm will move from node to node towards the end node. This is done by evaluating the neighbour nodes of the current node's position to decide in which direction the algorithm should step to reach the goal in the cheapest way possible. 
When all paths have been successfully created, the total path cost will be saved. Then the algorithm will sort the paths by cost and remove the most expensive paths; so the cheapest path remains intact. Subsequently, these removed paths are rerouted by the way explained above but starting in a different gate order and the start and goal node are swapped. If the total costs improved, the path combination is saved.
Then again is determined which of these new paths is the cheapest and the remaining paths are removed. This cycle repeats until there is 1 path left to be rerouted. After every cycle the algorithm checks if the total path costs improved.
The next step is removing all paths and rerouting the paths in the above manner with a different starting order of the gates; a "reset". Also when no solution is found for a path, a reset will follow.
The above process is repeated x number of times and when a path combination with a lower total cost is found, it is saved.

The explanation above can be summarised in the following steps:
- Route paths based on netlist order
- Remove most expensive paths
- Reroute paths in a different order and with swapped start and end nodes
- Save paths in a csv file if costs improved
- Repeat until there is 1 path left to be rerouted
- Remove all paths and restart the process above with a different order of the gates
- The existing csv will be overwritten and the cheapest path combination will be saved


## Running the program
### Running the algoritms
To run either of the two algorithms, their respective program needs to be run with the desired chip and netlist locations added as commandline arguments.

#### Algorithm 1:
At the commandprompt, enter:
python3 main_astar.py data/chip_{chipnumber of choice}/print_{number corresponding with the printplate of chosen chip}.csv data/chip_{chip of choice}/netlist_{number corresponding to the netlist of choice available for the chose chip}.csv

f.i., in the case of wanting to run netlist_1 from chip_0, type:
`python3 main_astar.py data/chip_0/print_0.csv data/chip_0/netlist_1.csv`

#### Algorithm 2:
At the commandprompt, enter:
python3 main_hill_climber.py data/chip_{chipnumber of choice}/print_{number corresponding with the printplate of chosen chip}.csv data/chip_{chip of choice}/netlist_{number corresponding to the netlist of choice available for the chose chip}.csv

f.i., in the case of wanting to run netlist_1 from chip_0, type:
`python3 main_hill_climber.py data/chip_0/print_0.csv data/chip_0/netlist_1.csv`

### Running the visualisation
After having run either of the algorithms in the manner described above, at the commandline enter:
`3d_model/manage.py runserver`
