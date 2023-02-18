import csv
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import pylab
import sys
import pandas as pd


# Returns a list of associated rows
def read_csv(file):
    file_data = []
    with open(file, mode='r', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Get header
        for row in csv_reader:
            assoc_row = dict()
            for i in range(len(header)):
                assoc_row[header[i]] = row[i]  # Make associative
            file_data.append(assoc_row)  # Add to data list
    return file_data


# Ask for user input
def get_paste():
    segments = []
    for line in sys.stdin:
        segments.append(line)
    return segments


# Parse x values
def parse_x(elements):
    x_out = dict()
    for elem in elements:
        count = 0
        for ch in elem:
            if ch == " ":
                count += 1
            else:
                break
        elem = elem[count:]
        pair = elem.split("  ")
        x_out[int(pair[0])] = int(pair[1])
    return x_out


# Parse y values
def parse_y(elements):
    y_out = []
    first = elements[0]
    columns = first[first.find("_") - 1:first.find("    ")].split()
    for i in range(1, len(elements)):
        y_out.append(map(lambda val: int(val), elements[i].split()[1:]))
    return pd.DataFrame(y_out, columns=columns).astype(int)


# Parses the AMPL output
def parse_output(inp):
    for i in range(0, len(inp)):
        inp[i] = inp[i].replace('\n', '')

    x_start = inp.index("x [*] :=") + 1
    x_end = inp.index(";")
    y_start = inp.index("y [*,*]") + 1
    y_end = len(inp) - 1

    return parse_x(inp[x_start:x_end]), parse_y(inp[y_start:y_end])


# Generates the graph
def build_graph():
    G = nx.Graph()
    color_options = ['r', 'g', 'b', 'y', 'm', 'black']

    current_color = 0
    color_map = dict()
    for edge in y.columns:
        n1 = int(edge.split("_")[0])
        n2 = int(edge.split("_")[1])

        # Center node colors
        n1_color = 'white'
        n2_color = 'white'
        if x[n1]:
            n1_color = 'grey'
        if x[n2]:
            n2_color = 'grey'

        # Add Nodes
        G.add_node(n1, pos=(node_data["X-Coordinate"][n1], node_data["Y-Coordinate"][n1]), node_color=n1_color)
        G.add_node(n2, pos=(node_data["X-Coordinate"][n2], node_data["Y-Coordinate"][n2]), node_color=n2_color)

        # Add edge and verify color
        color_index = y[y[edge] == 1].index[0]
        if color_index not in color_map:
            color_map[color_index] = color_options[current_color]
            current_color += 1
        G.add_edge(n1, n2, color=color_map[color_index], weight=3, node_size=1)

    # Get graph attributes
    pos = nx.get_node_attributes(G, 'pos')
    colors = nx.get_edge_attributes(G, 'color').values()
    weights = nx.get_edge_attributes(G, 'weight').values()
    node_colors = nx.get_node_attributes(G, 'node_color').values()

    # Save figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    plt.title(f"IEE574 n_171 Network", fontdict=dict(size=30))
    fig = plt.figure(1)
    nx.draw(G, pos,
            font_color='black',
            font_size=12,
            node_color=node_colors,
            node_size=250,
            edge_color=colors,
            width=list(weights),
            with_labels=True)
    plt.savefig("Output_Graph", bbox_inches="tight")
    pylab.close()
    del fig
    print("\nNetwork image saved to Output_Graph.png")


if __name__ == "__main__":
    print("\nPaste AMPL text below. Press ctrl+d when complete:\n")

    node_data = pd.DataFrame(read_csv("./Data_Files/NodeData.csv")).astype(int)

    # Ask for input and generate the network
    lines = get_paste()
    x, y = parse_output(lines)
    build_graph()
