import pandas as pd
import networkx as nx
import json

def set_filtered_users(csv_file):
    global filtered_users
    
    # Read data from CSV file
    data = pd.read_csv(csv_file)

    # Create directed graph
    G = nx.DiGraph()

    # Generate lists of unique users
    unique_users = set(data['User'])

    # Filter users based on the number of followers and followings
    filtered_users = [user for user in unique_users if 4 < len(eval(data[data['User'] == user]['Followers'].iloc[0])) < 201 and 4 < len(eval(data[data['User'] == user]['Following'].iloc[0])) < 201]

def generate_follow_network(csv_file):
    # Read data from CSV file
    data = pd.read_csv(csv_file)

    # Create directed graph
    G = nx.DiGraph()

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
                    
    return G

def generate_movie_network(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Filter the DataFrame based on the provided list of users
    df_filtered = df[df['User'].isin(filtered_users)]
    
    # Create a graph object
    G = nx.Graph()
    
    # Iterate through each movie and add edges between users who watched the same movie
    for movie in df_filtered['Movie'].unique():
        users_watched = df_filtered[df_filtered['Movie'] == movie]['User'].tolist()
        # Add edges between users who watched the same movie
        for i in range(len(users_watched)):
            for j in range(i + 1, len(users_watched)):
                if users_watched[i] != users_watched[j]:
                    # Check if an edge already exists between the two users
                    if G.has_edge(users_watched[i], users_watched[j]):
                        # If the edge exists, increase its weight by 1
                        G[users_watched[i]][users_watched[j]]['weight'] += 1
                    else:
                        # If the edge doesn't exist, add it with weight 1
                        G.add_edge(users_watched[i], users_watched[j], movie=movie, weight=1)
                
    return G

def generate_movie_liked_network(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Filter the DataFrame based on the provided list of users
    df_filtered = df[df['User'].isin(filtered_users)]
    
    # Create a graph object
    G = nx.Graph()
    
    # Add filtered users as nodes
    for user in filtered_users:
        G.add_node(user)
    
    # Iterate through each movie and add edges between users who watched the same movie
    for movie in df_filtered['Movie'].unique():
        liked_users = df_filtered[(df_filtered['Movie'] == movie) & (df_filtered['Liked'] == True)]['User'].tolist()
        # Add edges between users who liked the same movie
        for i in range(len(liked_users)):
            for j in range(i + 1, len(liked_users)):
                if liked_users[i] != liked_users[j]:
                    # Check if an edge already exists between the two users
                    if G.has_edge(liked_users[i], liked_users[j]):
                        # If the edge exists, increase its weight by 1
                        G[liked_users[i]][liked_users[j]]['weight'] += 1
                    else:
                        # If the edge doesn't exist, add it with weight 1
                        G.add_edge(liked_users[i], liked_users[j], movie=movie, weight=1)
                
    return G


def parse_all_data(follow_G, movie_json):
    # Load data from JSON file
    with open(movie_json, 'r') as file:
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
        num_followers.append(len(follow_G.in_edges(user_data['User'])))
        num_following.append(len(follow_G.out_edges(user_data['User'])))
        
    return num_reviews, num_movies_watched, num_followers, num_following
    
def get_watch_statistics(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Filter users that are included in the graph
    df_filtered = df[df['User'].isin(filtered_users)]

    # Calculate average number of movies watched per user
    average_movies_watched = df_filtered.groupby('User')['Movie'].nunique().mean()

    # Calculate average number of movies liked per user
    average_movies_liked = df_filtered[df_filtered['Liked'] == True].groupby('User')['Movie'].nunique().mean()

    # Get top 5 users based on movies watched
    top_users_movies_watched = df.groupby('User')['Movie'].nunique().nlargest(5)

    # Get top 5 users based on movies liked
    top_users_movies_liked = df_filtered[df_filtered['Liked'] == True].groupby('User')['Movie'].nunique().nlargest(5)
    
    return average_movies_watched, average_movies_liked, top_users_movies_watched, top_users_movies_liked
    
    
