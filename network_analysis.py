import networkx as nx

def analyze_network(G):
    # Compute network density
    density = nx.density(G)
    
    # Compute centrality measures
    eigenvector_centrality = nx.eigenvector_centrality_numpy(G)
    degree_centrality = nx.degree_centrality(G)
    pagerank_centrality = nx.pagerank(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # Clustering
    clustering_coefficients = nx.clustering(G)
    average_clustering = nx.average_clustering(G)
    
    # Nodal degree
    average_nodal_degree = sum(dict(G.degree()).values()) / len(G)
    
    return density, eigenvector_centrality, degree_centrality, pagerank_centrality, closeness_centrality, betweenness_centrality, clustering_coefficients, average_clustering, average_nodal_degree

def compute_distance_measures(G, graph_type):
    if graph_type == 'directed':
        # Compute diameter and average shortest path length for the directed graph
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

        # Diameter of the graph is the maximum diameter of its components
        diameter = max(diameters)
    else:
        # Compute diameter and average shortest path length for the undirected graph
        diameter = nx.diameter(G)
        avg_shortest_path_length = nx.average_shortest_path_length(G)      
    
    return avg_shortest_path_length, diameter
    
def get_top_5_users(G):
    degree_centrality = nx.degree_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality_numpy(G)
    pagerank_centrality = nx.pagerank(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # Get top 5 users for each centrality measure
    top_5_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_eigenvector = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_pagerank = sorted(pagerank_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "top_5_degree": top_5_degree,
        "top_5_eigenvector": top_5_eigenvector,
        "top_5_pagerank": top_5_pagerank,
        "top_5_closeness": top_5_closeness,
        "top_5_betweenness": top_5_betweenness
    }
    