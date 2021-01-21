from django.shortcuts import render
from django.http import HttpResponse
from json import dumps


# Create your views here.
def index(request):
    return render(request, "chips_and_circuits/index.html", { "message": "test11" })


def upload_csv(request):
    if "POST" == request.method:
        
        graph_data = []
        netlist_file = request.FILES["netlist_file"]
        
        netlist_data = netlist_file.read().decode("utf-8")   
        # print(netlist_data)
        netlist_data = netlist_data.replace('[[', '')
        netlist_data = netlist_data.replace(']]"', '')
        netlist_data = netlist_data.split('\r\n')
        # netlist_data = netlist_data.split('","')

        # print(netlist_data)
        for i in range(1, len(netlist_data) - 2):
            connect_data = netlist_data[i].split('","')
            coords_data = connect_data[1].split('], [')
            x = []
            y = []
            z = []
            graph_data.append([x,y,z,'lines'])

            for coords in coords_data:
                (x_coord, y_coord, z_coord) = coords.split(",")
                graph_data[i-1][0].append(x_coord)
                graph_data[i-1][1].append(y_coord)
                graph_data[i-1][2].append(z_coord)
                # print(graph_data)
                # print(coords_data[i])
                pass

            # print(coords_data)
            # print(f"con: {connect_data}")
            # for j in 
            # x = [source[0], goal[0]]
            # y = [source[1], goal[1]]
            # z = [source[2], goal[2]]


        dimension_file = request.FILES["dimensions_file"]
        dimension_file = dimension_file.read().decode("utf-8")  
        dimension_file = dimension_file.replace('\r\n', '')
        dimensions = dimension_file.split(",")
        print(dimensions)



        print_file = request.FILES["print_file"]
        print_data_string = print_file.read().decode("utf-8")   
        print(print_data_string)
        print_data_array = print_data_string.split("\n")  
        print_coordinates = []

        for i in range (1, len(print_data_array)):
            gate_data = print_data_array[i].split(",")
            if len(gate_data) > 1:
                gate_coordinate = [ 
                    [ gate_data[1] ],
                    [ gate_data[2] ],
                    ["3"],
                    'markers']
                graph_data.append(gate_coordinate)
    

        test1_JSON = dumps(print_data_array[1])
        test2_JSON = dumps(gate_data)
        graph_data_JSON = dumps(graph_data)
        settings_JSON = dumps(dimensions)

        return render(request, "chips_and_circuits/index.html", {
            "test1_JSON": test1_JSON,
            "test2_JSON": test2_JSON,
            "graph_data_JSON": graph_data_JSON,
            "settings_JSON": settings_JSON
        })


    else: 
        return render(request, "chips_and_circuits/index.html", { "message": "ELSE ERROR" })


