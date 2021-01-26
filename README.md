The first algorithm one can choose form is a `Best First Search` algorithm. To properly run this, the following command line has to be used and altered:
`python main.py print.csv netlist.csv`
Be sure to use the correct python call. The `print.csv` file has to be altered regarding the chip one wishes to use (print_0/print_1/print_2), while the `netlist.csv` file is altered to one of the netlists (netlist_1, netlist_2, etc).
The algorithm istelf then takes these inputs and processes them. The order of connections indicated in the netlist will be the first order that is used. After it is able to connect all the gates, or after it has made 10 attempt to do so but failed ten times, a new order will be initiated. This will be done four times and can be sumarised as follows:
- netlist order
- reversed netlist order
- smallest distance between gates to largest distance
- largest distance between gates to smallest distance
Each aformentioned attempt within one order will make a slight change. The gates which could not be connected by the algorithm will be removed from its original place in the list and moved to the front. This way it is certain that the they are able to connect after which it will attempt to connect the remainder of gates.
To further delve into the algorithm, after it has succeeded in connected two gates, it will not automatically use that path. It will retrace its steps to see if another, cheaper path is possible. Only when all the other options have been looked into, will it save the cheapest path.
If an connection order has been able to connect all gates, these results will be saved as a csv file. In the case that a later order manages to connect the gates with cheaper results, the existing csv will be overwritten and the cheapest will be saved.