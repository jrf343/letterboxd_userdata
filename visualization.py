import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd

def chart_follow_plots(num_reviews, num_movies_watched, num_followers, num_following, degree_centrality_values):
    # Plotting number of reviews vs number of followers
    plt.figure(figsize=(10, 6))
    plt.scatter(num_reviews, num_followers, color='blue', alpha=0.5)
    plt.xlabel('Number of Reviews')
    plt.ylabel('Number of Followers')
    plt.title('Number of Reviews vs Number of Followers')
    plt.grid(True)
    plt.show()

    # Plotting number of movies watched vs number of followers
    plt.figure(figsize=(10, 6))
    plt.scatter(num_movies_watched, num_followers, color='green', alpha=0.5)
    plt.xlabel('Number of Movies Watched')
    plt.ylabel('Number of Followers')
    plt.title('Number of Movies Watched vs Number of Followers')
    plt.grid(True)
    plt.show()

    # Plotting number of reviews vs number of movies watched
    plt.figure(figsize=(10, 6))
    plt.scatter(num_reviews, num_movies_watched, color='red', alpha=0.5)
    plt.xlabel('Number of Reviews')
    plt.ylabel('Number of Movies Watched')
    plt.title('Number of Reviews vs Number of Movies Watched')
    plt.grid(True)
    plt.show()
    
    # Plot activity (number of movie reviews) vs. connectivity
    plt.figure(figsize=(8, 6))
    plt.scatter(num_reviews, degree_centrality_values, alpha=0.5)
    plt.xlabel('Number of Movie Reviews')
    plt.ylabel('Connectivity (Degree Centrality)')
    plt.title('Number of Movie Reviews vs. Connectivity')
    plt.show()
    
def visualize_clusters(G, t):
    # Sociomatrix
    sociomatrix = nx.to_numpy_array(G)

    # Calculate pairwise distances for hierarchical clustering
    distance_matrix = ssd.pdist(sociomatrix, metric='euclidean')

    nodes_array = list(G.nodes())
    linkage_matrix = sch.linkage(distance_matrix, method='ward')

    # Perform clustering based on the dendrogram
    partition = sch.fcluster(linkage_matrix, t, criterion='distance')
    partition = dict(zip(nodes_array, partition))

    # Create a qualitative colormap for the clusters
    cmap = plt.get_cmap('tab10')
    
    # Get unique cluster IDs
    unique_clusters = set(partition.values())

    # Create a dictionary to store users in each cluster
    clusters = {cluster_id: [] for cluster_id in unique_clusters}
    
    # Populate the clusters dictionary
    for user, cluster_id in partition.items():
        clusters[cluster_id].append(user)
    
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
    plt.show()
    
    # Return clusters dictionary
    return clusters

    
def visualize_dendrogram(G):
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
    plt.show()
    
def generate_movie_graph_ml(G):
    # Export to GraphML file
    graphml_file_path = "movie_data.graphml"
    nx.write_graphml(G, graphml_file_path)

    print(f"Graph data exported to {graphml_file_path}")
    
def generate_liked_graph_ml(G):
    # Export to GraphML file
    graphml_file_path = "movie_liked_data.graphml"
    nx.write_graphml(G, graphml_file_path)

    print(f"Graph data exported to {graphml_file_path}")
    
def generate_follow_graph_ml(G):
    # Export to GraphML file
    graphml_file_path = "follow_data.graphml"
    nx.write_graphml(G, graphml_file_path)

    print(f"Graph data exported to {graphml_file_path}")