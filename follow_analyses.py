import data_processing
import network_analysis
import visualization

follow_csv = './output_data/output_follow_information.csv'
movie_json = './output_data/output_movies_information.json'

data_processing.set_filtered_users(follow_csv)

G = data_processing.generate_follow_network(follow_csv)
#visualization.generate_follow_graph_ml(G)

density, eigenvector_centrality, degree_centrality, pagerank_centrality, closeness_centrality, betweenness_centrality, clustering_coefficients, average_clustering, average_nodal_degree = network_analysis.analyze_network(G)

print(f"\nNetwork Density: {density}")
print(f"\nAverage Clustering Coefficient: {average_clustering}")
print(f"\nAverage Eigenvector Centrality: {sum(eigenvector_centrality.values()) / len(G)}")
print(f"\nAverage Degree Centrality: {sum(degree_centrality.values()) / len(G)}")
print(f"\nAverage PageRank Centrality: {sum(pagerank_centrality.values()) / len(G)}")
print(f"\nAverage Nodal Degree: {average_nodal_degree}")
print(f"\nAverage Closeness Centrality: {sum(closeness_centrality.values()) / len(G)}")
print(f"\nAverage Betweenness Centrality: {sum(betweenness_centrality.values()) / len(G)}")

num_reviews, num_movies_watched, num_followers, num_following = data_processing.parse_all_data(G, movie_json)

# Extracting centrality values from dictionary
degree_centrality_values = list(degree_centrality.values())

visualization.chart_follow_plots(num_reviews, num_movies_watched, num_followers, num_following, degree_centrality_values)

avg_shortest_path_length, diameter = network_analysis.compute_distance_measures(G, 'directed')

print("\nAverage Shortest Path Length:", avg_shortest_path_length)
print("\nDiameter of the directed graph (max among SCCs):", diameter)

top_users = network_analysis.get_top_5_users(G)
print("\nTop Users:")
print(top_users)