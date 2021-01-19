let traces = [];
 
console.log(graph_data);
console.log(test1_JSON);
console.log(test2_JSON);

lines_xyz = graph_data;
dimensions = settings_data;

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
    // autosize: false,
        width: 1000,
        height: 700,
        xaxis: {
            // autotick: false,
            // ticks: 'outside',
            // tick0: 0,
            // dtick: 0.25,
            // ticklen: 8,
            // tickwidth: 4,
            // tickmode: 'linear',
            // tick0: 0,
            // dtick: 1,
            range: [parseInt(dimensions[0]), 0]
        },
        yaxis: {
            // tickmode: 'linear',
            // tick0: 0,
            // dtick: 1,
            range: [parseInt(dimensions[1]), 0]
        },
        zaxis: {
            // tickmode: 'linear',
            // tick0: 0,
            // dtick: 1,
            range: [0, parseInt(dimensions[2])]
        }},
};
Plotly.newPlot('graph_div', data, layout); 
