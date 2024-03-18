import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Function to extract followers and following
def extract_follow_data(file_path):
    # Define a deque with a maximum length of 6
    last_6_lines = deque(maxlen=6)

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Iterate through each line in the file
        for line in file:
            # Decode the line and strip whitespace
            decoded_line = line.decode().strip()

            # Add the decoded line to the deque
            last_6_lines.append(decoded_line)

    # Extract the required information from the last 6 rows
    followers_line = last_6_lines[-4]
    following_line = last_6_lines[-1]

    # Split the lines to get followers and following
    followers = followers_line.split(',')
    following = following_line.split(',')

    # Extract username from the filename without extension
    user = os.path.splitext(os.path.basename(file_path))[0]
    user = user[:-5]  # Subtract the last 5 characters

    return user, followers, following

# Path to the folder containing user data files
folder_path = "userdata/"

# List all CSV files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Original user list from file names
original_users = set(os.path.splitext(f)[0][:-5] for f in files)

# Set to store unique users
unique_users = set()

# List to store edges of the graph
edges = []

# Process each file
for file in files:
    user, followers, following = extract_follow_data(os.path.join(folder_path, file))

    # Add user to set if it's in the original list
    if (0 < len(followers)) and (0 < len(following)) and (user in original_users):
        unique_users.add(user)

        # Add edges to the graph for users in the original list
        for follower in followers:
            if follower in original_users:
                edges.append((follower, user))  # Reverse the order to represent follower -> user

        for followee in following:
            if followee in original_users:
                edges.append((user, followee))  # Keep the order as user -> followee

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
G.add_nodes_from(unique_users)
G.add_edges_from(edges)

# Export to GraphML file
graphml_file_path = "follow_data.graphml"
nx.write_graphml(G, graphml_file_path)

print(f"Graph data exported to {graphml_file_path}")