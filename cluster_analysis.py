import data_processing
import visualization
from sklearn.metrics import adjusted_rand_score

def check_rand_index(clusters_A, clusters_B):
    # Assign unique labels to clusters
    labels_networkA = [idx for idx, cluster in enumerate(clusters_A.values()) for _ in cluster]
    labels_networkB = [idx for idx, cluster in enumerate(clusters_B.values()) for _ in cluster]

    # Compute Adjusted Rand Index
    ari = adjusted_rand_score(labels_networkA, labels_networkB)
    
    return ari

follow_csv = './output_data/output_follow_information.csv'
movie_csv = './output_data/output_movies_information.csv'

data_processing.set_filtered_users(follow_csv)

G_follow = data_processing.generate_follow_network(follow_csv)

visualization.visualize_dendrogram(G_follow)
clusters_follow = visualization.visualize_clusters(G_follow, 8)

G_watched = data_processing.generate_movie_network(movie_csv)

visualization.visualize_dendrogram(G_watched)
clusters_watched = visualization.visualize_clusters(G_watched, 1500)

ari_follow_watched = check_rand_index(clusters_follow, clusters_watched)
print("ARI for follow and watched networks:", ari_follow_watched)

G_liked = data_processing.generate_movie_liked_network(movie_csv)

visualization.visualize_dendrogram(G_liked)
clusters_liked = visualization.visualize_clusters(G_liked, 300)

ari_follow_liked = check_rand_index(clusters_follow, clusters_liked)
print("ARI for follow and liked networks:", ari_follow_liked)