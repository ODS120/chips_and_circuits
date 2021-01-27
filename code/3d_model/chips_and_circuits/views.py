"""
views.py

Chips & Circuits 2021
Martijn van Veen, Olaf Stringer, Jan-Joost Raedts

Load a webpage which processes data files from the Chips & Circuits case
on which a graph can be seen that visualises the connected gates on the chip.
"""


from json import dumps
from django.shortcuts import render


def index(request):
    """
    Load a page on which two files can be loaded.
    """
    return render(request, "chips_and_circuits/index.html")


def upload_csv(request):
    """
    Processes the information necessary to visualise the 3d graph of the
    connected gates.
    """
    if request.method == "POST":
        # Prepare the output.csv file
        graph_data = []
        netlist_file = request.FILES["netlist_file"]
        netlist_data = netlist_file.read().decode("utf-8")
        netlist_data = netlist_data.replace('"(', '')
        netlist_data = netlist_data.replace(')]"', '')
        netlist_data = netlist_data.split('\r\n')

        # Put the data in an array
        for i in range(1, len(netlist_data) - 2):
            connect_data = netlist_data[i].split('","[(')
            coords_data = connect_data[1].split('), (')

            # Initialise the coordinates
            x = []
            y = []
            z = []
            graph_data.append([x,y,z,'lines'])

            for coords in coords_data:
                (x_coord, y_coord, z_coord) = coords.split(",")
                graph_data[i-1][0].append(x_coord)
                graph_data[i-1][1].append(y_coord)
                graph_data[i-1][2].append(z_coord)

        # Prepare the chip file
        print_file = request.FILES["print_file"]
        print_data_string = print_file.read().decode("utf-8")   
        print_data_array = print_data_string.split("\n")

        x_axis_limit = 0
        y_axis_limit = 0
        z_axis_limit = '7'

        # Put the data in an array
        for i in range (1, len(print_data_array)):
            gate_data = print_data_array[i].split(",")

            if len(gate_data) > 1:
                # Check for the highest values
                if int(gate_data[1]) > x_axis_limit:
                    x_axis_limit = int(gate_data[1])

                if int(gate_data[2]) > y_axis_limit:
                    y_axis_limit = int(gate_data[2])

                gate_coordinate = [ 
                    [ gate_data[1] ],
                    [ gate_data[2] ],
                    ["0"],
                    'markers']
                graph_data.append(gate_coordinate)

        limits = [str(x_axis_limit + 2), str(y_axis_limit + 2), z_axis_limit]
        print(graph_data)
        return render(request, "chips_and_circuits/index.html", {
            "graph_data_JSON": dumps(graph_data),
            "settings_JSON": dumps(limits)
        })

    return render(request, "chips_and_circuits/index.html", { "message": "ELSE ERROR" })