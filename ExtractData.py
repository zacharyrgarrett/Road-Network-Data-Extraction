# ExtractData.py
# Author: Zachary Garrett
# Description: Extracts the parameter d_i,(j,k) for each node-edge pair. Outputs to .csv and .txt

import csv
import math
import pandas as pd


# Global Variables
node_data = []
edge_data = []
parameter_data = []
edge_labels = []


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


# Computes the midpoint
# Sample Row: {'Node 1': '0', 'Node 2': '1', 'ID': '01', 'X-Midpoint': -11696659.5, 'Y-Midpoint': 3279920.0}
def compute_midpoints():
    global node_data, edge_data, edge_labels
    updated_data = []
    for edge in edge_data:
        n1 = int(edge["Node 1"])
        n2 = int(edge["Node 2"])
        edge_labels.append(f"{n1}_{n2}")
        edge["ID"] = f"{n1}_{n2}"
        edge["X-Midpoint"] = 0.5 * (float(node_data[n1]["X-Coordinate"]) + float(node_data[n2]["X-Coordinate"]))
        edge["Y-Midpoint"] = 0.5 * (float(node_data[n1]["Y-Coordinate"]) + float(node_data[n2]["Y-Coordinate"]))
        updated_data.append(edge)
    edge_data = updated_data


# Loops through each node-edge pair and computes the parameters
def extract_parameters():
    global node_data, edge_data, parameter_data
    node_data = read_csv("NodeData.csv")
    edge_data = read_csv("EdgeData.csv")
    compute_midpoints()

    for node in node_data:      # Loop through each node
        node_row = []
        for edge in edge_data:  # Loop through each edge
            a = float(node["X-Coordinate"]) - float(edge["X-Midpoint"])
            b = float(node["Y-Coordinate"]) - float(edge["Y-Midpoint"])
            c = math.sqrt(pow(a, 2) + pow(b, 2))
            node_row.append(c)
        parameter_data.append(node_row)
    return


if __name__ == '__main__':
    extract_parameters()
    df = pd.DataFrame(parameter_data, columns=[edge_labels]).transpose()
    df.to_csv("n_171_OUTPUT.csv")
    df.to_csv("n_171_OUTPUT.txt", sep=" ")
    print("Done")
