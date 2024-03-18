import data_processing
import network_analysis
import visualization

follow_csv = './output_data/output_follow_information.csv'
movie_csv = './output_data/output_movies_information.csv'

data_processing.set_filtered_users(follow_csv)

G_watched = data_processing.generate_movie_network(movie_csv)
#visualization.generate_movie_graph_ml(G_watched)

density, eigenvector_centrality, degree_centrality, pagerank_centrality, closeness_centrality, betweenness_centrality, clustering_coefficients, average_clustering, average_nodal_degree = network_analysis.analyze_network(G_watched)

print(f"\nNetwork Density: {density}")
print(f"\nAverage Clustering Coefficient: {average_clustering}")
print(f"\nAverage Eigenvector Centrality: {sum(eigenvector_centrality.values()) / len(G_watched)}")
print(f"\nAverage Degree Centrality: {sum(degree_centrality.values()) / len(G_watched)}")
print(f"\nAverage PageRank Centrality: {sum(pagerank_centrality.values()) / len(G_watched)}")
print(f"\nAverage Nodal Degree: {average_nodal_degree}")
print(f"\nAverage Closeness Centrality: {sum(closeness_centrality.values()) / len(G_watched)}")
print(f"\nAverage Betweenness Centrality: {sum(betweenness_centrality.values()) / len(G_watched)}")

avg_shortest_path_length, diameter = network_analysis.compute_distance_measures(G_watched, 'undirected')

print("\nAverage Shortest Path Length:", avg_shortest_path_length)
print("\nDiameter of the undirected graph:", diameter)

top_users = network_analysis.get_top_5_users(G_watched)
print("\nTop Users:")
print(top_users)

G_liked = data_processing.generate_movie_liked_network(movie_csv)
#visualization.generate_liked_graph_ml(G_liked)

density, eigenvector_centrality, degree_centrality, pagerank_centrality, closeness_centrality, betweenness_centrality, clustering_coefficients, average_clustering, average_nodal_degree = network_analysis.analyze_network(G_liked)

print(f"\nNetwork Density: {density}")
print(f"\nAverage Clustering Coefficient: {average_clustering}")
print(f"\nAverage Eigenvector Centrality: {sum(eigenvector_centrality.values()) / len(G_liked)}")
print(f"\nAverage Degree Centrality: {sum(degree_centrality.values()) / len(G_liked)}")
print(f"\nAverage PageRank Centrality: {sum(pagerank_centrality.values()) / len(G_liked)}")
print(f"\nAverage Nodal Degree: {average_nodal_degree}")
print(f"\nAverage Closeness Centrality: {sum(closeness_centrality.values()) / len(G_liked)}")
print(f"\nAverage Betweenness Centrality: {sum(betweenness_centrality.values()) / len(G_liked)}")

top_users = network_analysis.get_top_5_users(G_liked)
print("\nTop Users:")
print(top_users)

average_movies_watched, average_movies_liked, top_users_movies_watched, top_users_movies_liked = data_processing.get_watch_statistics(movie_csv)

# Print the average number of movies watched and liked
print("Average number of movies watched per user:", average_movies_watched)
print("Average number of movies liked per user:", average_movies_liked)
# Print the top 5 users based on movies watched
print("\nTop 5 users based on movies watched:")
print(top_users_movies_watched)

# Print the top 5 users based on movies liked
print("\nTop 5 users based on movies liked:")
print(top_users_movies_liked)