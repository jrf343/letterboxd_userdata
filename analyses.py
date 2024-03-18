import pandas as pd
import networkx as nx
import json
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd

# Read data from CSV file
data = pd.read_csv('./output_data/output_follow_information.csv')

# Create directed graph
G = nx.DiGraph()

# Generate lists of unique users
unique_users = set(data['User'])
print('Number Unique Users: ', len(unique_users))

# Filter users based on the number of followers and followings
filtered_users = [user for user in unique_users if 4 < len(eval(data[data['User'] == user]['Followers'].iloc[0])) < 201 and 4 < len(eval(data[data['User'] == user]['Following'].iloc[0])) < 201]

# Add nodes and edges to the graph
for index, row in data.iterrows():
    user = row['User']
    if user in filtered_users:
        followers = eval(row['Followers'])
        following = eval(row['Following'])
        G.add_node(user)
        for follower in followers:
            if follower in filtered_users:
                G.add_edge(follower, user)
        for followee in following:
            if followee in filtered_users:
                G.add_edge(user, followee)
                
print("\nNumber of Nodes:", G.number_of_nodes())

# Compute network density
density = nx.density(G)
print(f"\nNetwork Density: {density}")

# Compute measures for the entire graph
eigenvector_centrality = nx.eigenvector_centrality_numpy(G)
degree_centrality = nx.degree_centrality(G)
pagerank_centrality = nx.pagerank(G)

# Hierarchical clustering
clustering_coefficients = nx.clustering(G)
average_clustering = nx.average_clustering(G)
print(f"\nAverage Clustering Coefficient: {average_clustering}")

# Nodal degree
average_nodal_degree = sum(dict(G.degree()).values()) / len(G)

# Closeness centrality
closeness_centrality = nx.closeness_centrality(G)

# Betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)

# Display results
print(f"\nAverage Eigenvector Centrality: {sum(eigenvector_centrality.values()) / len(G)}")
print(f"\nAverage Degree Centrality: {sum(degree_centrality.values()) / len(G)}")
print(f"\nAverage PageRank Centrality: {sum(pagerank_centrality.values()) / len(G)}")
print(f"\nAverage Nodal Degree: {average_nodal_degree}")
print(f"\nAverage Closeness Centrality: {sum(closeness_centrality.values()) / len(G)}")
print(f"\nAverage Betweenness Centrality: {sum(betweenness_centrality.values()) / len(G)}")

# Load data from JSON file
with open('./output_data/output_movies_information.json', 'r') as file:
    movie_data = json.load(file)

# Filter users that are included in the graph
filtered_movie_data = [user_data for user_data in movie_data if user_data['User'] in filtered_users]

# Initialize lists to store data for plotting
num_reviews = []
num_movies_watched = []
num_followers = []
num_following = []

# Iterate over each user's movie data
for user_data in filtered_movie_data:
    # Count the number of movies with reviews
    reviewed_movies = [movie for movie in user_data['Movies'] if movie['Review'] is not None]
    num_reviews.append(len(reviewed_movies))
    
    num_movies_watched.append(len(user_data['Movies']))
    num_followers.append(len(G.in_edges(user_data['User'])))
    num_following.append(len(G.out_edges(user_data['User'])))

# Plotting number of reviews vs number of followers
plt.figure(figsize=(10, 6))
plt.scatter(num_reviews, num_followers, color='blue', alpha=0.5)
plt.xlabel('Number of Reviews')
plt.ylabel('Number of Followers')
plt.title('Number of Reviews vs Number of Followers')
plt.grid(True)
#plt.show()

# Plotting number of movies watched vs number of followers
plt.figure(figsize=(10, 6))
plt.scatter(num_movies_watched, num_followers, color='green', alpha=0.5)
plt.xlabel('Number of Movies Watched')
plt.ylabel('Number of Followers')
plt.title('Number of Movies Watched vs Number of Followers')
plt.grid(True)
#plt.show()

# Plotting number of reviews vs number of movies watched
plt.figure(figsize=(10, 6))
plt.scatter(num_reviews, num_movies_watched, color='red', alpha=0.5)
plt.xlabel('Number of Reviews')
plt.ylabel('Number of Movies Watched')
plt.title('Number of Reviews vs Number of Movies Watched')
plt.grid(True)
#plt.show()

# Extracting centrality values from dictionary
degree_centrality_values = list(degree_centrality.values())

# Plot activity (number of movie reviews) vs. connectivity
plt.figure(figsize=(8, 6))
plt.scatter(num_reviews, degree_centrality_values, alpha=0.5)
plt.xlabel('Number of Movie Reviews')
plt.ylabel('Connectivity (Degree Centrality)')
plt.title('Number of Movie Reviews vs. Connectivity')
#plt.show()

# Compute diameter and average shortest path length for the undirected graph
diameters = []
scc = list(nx.strongly_connected_components(G))
for component in scc:
    subgraph = G.subgraph(component)
    diameter = nx.diameter(subgraph)
    diameters.append(diameter)
    
avg_shortest_path_lengths = []
scc = list(nx.strongly_connected_components(G))
for component in scc:
    subgraph = G.subgraph(component)
    avg_shortest_path_lengths.append(nx.average_shortest_path_length(subgraph))

# Take the average of average shortest path lengths among the SCCs
avg_shortest_path_length = sum(avg_shortest_path_lengths) / len(avg_shortest_path_lengths)
print("\nAverage Shortest Path Length:", avg_shortest_path_length)

# Diameter of the graph is the maximum diameter of its components
diameter = max(diameters)
print("\nDiameter of the directed graph (max among SCCs):", diameter)

def visualize_clusters(G, partition):
    # Create a qualitative colormap for the clusters
    cmap = plt.get_cmap('tab10')
    
    # Get unique cluster IDs
    unique_clusters = set(partition.values())
    
    # Choose a layout for better visualization
    layout = nx.kamada_kawai_layout(G)
    
    # Plot the graph with nodes colored by their cluster
    plt.figure(figsize=(10, 8))
    for cluster_id in unique_clusters:
        nodes_in_cluster = [node for node, cluster in partition.items() if cluster == cluster_id]
        nx.draw_networkx_nodes(G, layout, nodelist=nodes_in_cluster, node_color=[cmap(cluster_id)], node_size=10, alpha=0.8)
    nx.draw_networkx_edges(G, layout, width=0.5, alpha=0.5)
    plt.title('Network Graph with Clusters')
    plt.axis('off')
    #plt.show()

# Sociomatrix
sociomatrix = nx.to_numpy_array(G)

# Calculate pairwise distances for hierarchical clustering
distance_matrix = ssd.pdist(sociomatrix, metric='euclidean')

# Plot dendrogram
nodes_array = list(G.nodes())
linkage_matrix = sch.linkage(distance_matrix, method='ward')
dendrogram = sch.dendrogram(linkage_matrix, labels=nodes_array)
plt.xlabel('Actors')
plt.ylabel('Pairise (Euclidan) Distance')
#plt.show()

# Perform clustering based on the dendrogram
partition = sch.fcluster(linkage_matrix, t=8, criterion='distance')  # Adjust the threshold 't' as needed

# Visualize clusters on the network graph
visualize_clusters(G, dict(zip(nodes_array, partition)))

# common movies within clusters
for cluster_id in set(partition):
    cluster_users = [user for user, cluster in zip(nodes_array, partition) if cluster == cluster_id]
    print(cluster_users)
    
    # Extract movie lists for users in the cluster
    cluster_movie_lists = [user_data['Movies'] for user_data in movie_data if user_data['User'] in cluster_users]
    
    # Flatten the list of dictionaries into a list of movie titles
    cluster_movies = [movie['Movie'] for movie_list in cluster_movie_lists for movie in movie_list]
    
    # Find common movies among users in the cluster
    common_movies = set(cluster_movies)
    for movie_list in cluster_movie_lists[1:]:
        common_movies = common_movies.intersection(set(movie['Movie'] for movie in movie_list))
    
    print(f"Cluster {cluster_id} has {len(common_movies)} common movies: {common_movies}")