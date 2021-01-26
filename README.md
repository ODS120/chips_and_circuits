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
