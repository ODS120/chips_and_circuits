let traces = [];
 
lines_xyz = graph_data;
dimensions = settings_data;
console.log(graph_data)
console.log(settings_data)

for (i = 0; i < lines_xyz.length; i++) {
    
    traces[i] = {
        x: lines_xyz[i][0],
        y: lines_xyz[i][1],
        z: lines_xyz[i][2],
    marker: {
        symbol: "circle",
        color: "#0028ed",
        size: 10,
    },
    line: {
        width: 5,
        color: "#ff0000",
    },
    mode: lines_xyz[i][3],
    type: "scatter3d"
    };
}
console.log(parseInt(dimensions[0]))
let data = traces;
let layout = {
    title: "Chips and Circuits",
    scene: {
        aspectmode: "manual",
        width: 1000,
        height: 600,
        xaxis: {
            range: [parseInt(dimensions[0]), 0]
        },
        yaxis: {
            range: [parseInt(dimensions[1]), 0]
        },
        zaxis: {
            range: [0, parseInt(dimensions[2])]
        }},
};
Plotly.newPlot('graph_div', data, layout); 